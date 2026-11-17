import { BUILD_CATEGORIES, bySlug } from './kb.js';

const REQUIRED = BUILD_CATEGORIES.map((category) => category.key);

const FIELD_RULES = {
  cpu: [
    ['socket', 'Сокет'],
    ['tdpW', 'TDP'],
    ['memoryType', 'Тип памяти']
  ],
  motherboard: [
    ['socket', 'Сокет'],
    ['memoryType', 'Тип памяти'],
    ['formFactor', 'Форм-фактор']
  ],
  gpu: [
    ['tdpW', 'TBP'],
    ['connectors', 'Разъёмы питания'],
    ['gpuLengthMm', 'Длина GPU']
  ],
  memory: [
    ['memoryType', 'Тип памяти'],
    ['ramCapacityGb', 'Объём'],
    ['ramHeightMm', 'Высота модулей']
  ],
  psu: [
    ['psuW', 'Мощность'],
    ['psu8pin', '8-pin PCIe'],
    ['psuAtx3', 'ATX 3.x']
  ],
  cooling: [
    ['sockets', 'Сокеты'],
    ['coolerTdp', 'TDP-рейтинг'],
    ['coolerHeightMm', 'Высота / радиатор']
  ],
  case: [
    ['caseForms', 'Форм-факторы'],
    ['caseGpuMaxMm', 'Лимит GPU'],
    ['caseCoolerMaxMm', 'Лимит кулера'],
    ['casePsuMaxMm', 'Лимит БП']
  ],
  storage: [['capacityGb', 'Объём']]
};

const STATUS_ORDER = { fail: 0, warn: 1, unknown: 2, pass: 3 };

function isKnown(value, field) {
  if (field === 'connectors') return Boolean(value && (value.eight > 0 || value.twelve));
  if (typeof value === 'boolean') return true;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === 'number') return Number.isFinite(value) && value > 0;
  return value !== null && value !== undefined && value !== '';
}

function measurement(measurements, key, fallback) {
  const raw = measurements?.[key];
  const value = typeof raw === 'string' ? Number(raw) : raw;
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

function selectedComponents(selection) {
  const result = {};
  for (const key of REQUIRED) {
    result[key] = selection[key] ? bySlug.get(selection[key]) : null;
  }
  return result;
}

function profileConflicts(selection, intentId) {
  const conflicts = [];
  let optimal = 0;
  let checked = 0;

  if (!intentId) return { optimal, checked, conflicts };

  for (const key of REQUIRED) {
    const component = bySlug.get(selection[key]);
    if (!component || !component.profiles.length) continue;
    checked += 1;

    for (const profile of component.profiles) {
      if (profile.optimal.includes(intentId)) optimal += 1;
      if (profile.failure.includes(intentId)) {
        conflicts.push({
          severity: profile.severity === 'BLOCK' ? 'fail' : 'warn',
          component: component.title,
          title: `Профиль ${profile.name}`,
          detail:
            profile.failureMode ||
            `Компонент не оптимален для интента ${intentId}.`
        });
      }
    }
  }

  return { optimal, checked, conflicts };
}

export function assessBuild(selection, intentId, budget = null, measurements = {}) {
  const parts = selectedComponents(selection);
  const checks = [];
  const missing = REQUIRED.filter((key) => !parts[key]);

  function add(id, label, status, detail, component = 'Сборка', critical = false) {
    checks.push({ id, label, status, detail, component, critical });
  }

  if (missing.length) {
    const labels = missing
      .map((key) => BUILD_CATEGORIES.find((category) => category.key === key)?.label || key)
      .join(', ');
    add('selection', 'Состав сборки', 'warn', `Не выбрано: ${labels}.`, 'Сборка');
  } else {
    add('selection', 'Состав сборки', 'pass', 'Все восемь категорий выбраны.');
  }

  const cpu = parts.cpu;
  const motherboard = parts.motherboard;
  const gpu = parts.gpu;
  const memory = parts.memory;
  const psu = parts.psu;
  const cooling = parts.cooling;
  const pcCase = parts.case;

  const gpuLength = measurement(measurements, 'gpuLengthMm', gpu?.norm.gpuLengthMm);
  const coolerHeight = measurement(measurements, 'coolerHeightMm', cooling?.norm.coolerHeightMm);
  const psuLength = measurement(measurements, 'psuLengthMm', psu?.norm.psuLengthMm);
  const ramHeight = measurement(measurements, 'ramHeightMm', memory?.norm.ramHeightMm);

  // CPU ↔ motherboard socket
  if (!cpu || !motherboard) {
    add('socket', 'Сокет CPU ↔ плата', 'unknown', 'Нужны CPU и материнская плата.');
  } else if (!cpu.norm.socket || !motherboard.norm.socket) {
    add('socket', 'Сокет CPU ↔ плата', 'unknown', 'В одной из карточек не указан сокет.', 'CPU ↔ плата', true);
  } else if (cpu.norm.socket !== motherboard.norm.socket) {
    add('socket', 'Сокет CPU ↔ плата', 'fail', `${cpu.title}: ${cpu.norm.socket}; ${motherboard.title}: ${motherboard.norm.socket}.`, 'CPU ↔ плата');
  } else {
    add('socket', 'Сокет CPU ↔ плата', 'pass', `${cpu.norm.socket}.`);
  }

  // Memory type
  const memoryTypes = [
    ['CPU', cpu?.norm.memoryType, cpu?.title],
    ['плата', motherboard?.norm.memoryType, motherboard?.title],
    ['модуль', memory?.norm.memoryType, memory?.title]
  ].filter(([, type]) => type);
  if (memoryTypes.length < 2) {
    add('memory', 'Тип памяти', 'unknown', 'Нужны хотя бы два источника типа памяти.', 'Память', true);
  } else if (new Set(memoryTypes.map(([, type]) => type)).size > 1) {
    add('memory', 'Тип памяти', 'fail', memoryTypes.map(([label, type, title]) => `${label} ${title}: ${type}`).join('; '), 'Память');
  } else {
    add('memory', 'Тип памяти', 'pass', memoryTypes[0][1]);
  }

  // Motherboard form factor
  if (!motherboard || !pcCase) {
    add('formfactor', 'Форм-фактор платы ↔ корпус', 'unknown', 'Нужны плата и корпус.');
  } else if (!motherboard.norm.formFactor || !pcCase.norm.caseForms.length) {
    add('formfactor', 'Форм-фактор платы ↔ корпус', 'unknown', 'В карточке нет поддержки форм-факторов.', 'плата ↔ корпус', true);
  } else if (!pcCase.norm.caseForms.includes(motherboard.norm.formFactor)) {
    add('formfactor', 'Форм-фактор платы ↔ корпус', 'fail', `${motherboard.norm.formFactor} не в списке: ${pcCase.norm.caseForms.join(', ')}.`, 'плата ↔ корпус');
  } else {
    add('formfactor', 'Форм-фактор платы ↔ корпус', 'pass', `${motherboard.norm.formFactor} поддерживается.`);
  }

  // Cooler socket
  if (!cpu || !cooling) {
    add('cooler-socket', 'Сокет кулера', 'unknown', 'Нужны CPU и охлаждение.');
  } else if (!cpu.norm.socket || !cooling.norm.sockets.length) {
    add('cooler-socket', 'Сокет кулера', 'unknown', 'Нет данных о сокете кулера.', 'CPU ↔ охлаждение', true);
  } else if (!cooling.norm.sockets.includes(cpu.norm.socket)) {
    add('cooler-socket', 'Сокет кулера', 'fail', `${cooling.title}: ${cooling.norm.sockets.join(', ')}; нужен ${cpu.norm.socket}.`, 'CPU ↔ охлаждение');
  } else {
    add('cooler-socket', 'Сокет кулера', 'pass', `${cpu.norm.socket}.`);
  }

  // Cooler height / radiator
  const isLiquid = cooling && (cooling.norm.layoutType.includes('liquid') || cooling.norm.layoutType.includes('aio') || cooling.norm.radiatorMm);
  if (!cooling || !pcCase) {
    add('cooler-height', 'Кулер ↔ корпус', 'unknown', 'Нужны охлаждение и корпус.');
  } else if (isLiquid) {
    if (!cooling.norm.radiatorMm || !pcCase.norm.caseRadiatorMm) {
      add('cooler-height', 'Радиатор СЖО ↔ корпус', 'unknown', 'Нет данных о поддержке радиатора.', 'охлаждение ↔ корпус', true);
    } else if (cooling.norm.radiatorMm > pcCase.norm.caseRadiatorMm) {
      add('cooler-height', 'Радиатор СЖО ↔ корпус', 'fail', `${cooling.norm.radiatorMm} мм при максимуме ${pcCase.norm.caseRadiatorMm} мм.`, 'охлаждение ↔ корпус');
    } else {
      add('cooler-height', 'Радиатор СЖО ↔ корпус', 'pass', `${cooling.norm.radiatorMm} мм ≤ ${pcCase.norm.caseRadiatorMm} мм.`);
    }
  } else if (!coolerHeight || !pcCase.norm.caseCoolerMaxMm) {
    add('cooler-height', 'Высота кулера ↔ корпус', 'unknown', 'Введите высоту кулера или лимит корпуса вручную.', 'охлаждение ↔ корпус', true);
  } else if (coolerHeight > pcCase.norm.caseCoolerMaxMm) {
    add('cooler-height', 'Высота кулера ↔ корпус', 'fail', `${coolerHeight} мм при лимите ${pcCase.norm.caseCoolerMaxMm} мм.`, 'охлаждение ↔ корпус');
  } else {
    add('cooler-height', 'Высота кулера ↔ корпус', 'pass', `${coolerHeight} мм ≤ ${pcCase.norm.caseCoolerMaxMm} мм.`);
  }

  // Cooler RAM clearance
  if (!cooling || !memory || isLiquid) {
    add('cooler-ram', 'Кулер ↔ высота RAM', 'unknown', 'Нужны воздушный кулер и модули памяти.');
  } else if (!cooling.norm.coolerRamClearanceMm || !ramHeight) {
    add('cooler-ram', 'Кулер ↔ высота RAM', 'unknown', 'Введите высоту модулей или клиренс кулера.', 'охлаждение ↔ память', true);
  } else if (ramHeight > cooling.norm.coolerRamClearanceMm) {
    add('cooler-ram', 'Кулер ↔ высота RAM', 'warn', `${ramHeight} мм при клиренсе ${cooling.norm.coolerRamClearanceMm} мм.`, 'охлаждение ↔ память');
  } else {
    add('cooler-ram', 'Кулер ↔ высота RAM', 'pass', `${ramHeight} мм ≤ ${cooling.norm.coolerRamClearanceMm} мм.`);
  }

  // GPU length
  if (!gpu || !pcCase) {
    add('gpu-length', 'Длина GPU ↔ корпус', 'unknown', 'Нужны видеокарта и корпус.');
  } else if (!gpuLength || !pcCase.norm.caseGpuMaxMm) {
    add('gpu-length', 'Длина GPU ↔ корпус', 'unknown', 'Введите длину видеокарты вручную — в карточке её нет.', 'GPU ↔ корпус', true);
  } else if (gpuLength > pcCase.norm.caseGpuMaxMm) {
    add('gpu-length', 'Длина GPU ↔ корпус', 'fail', `${gpuLength} мм при лимите ${pcCase.norm.caseGpuMaxMm} мм.`, 'GPU ↔ корпус');
  } else {
    add('gpu-length', 'Длина GPU ↔ корпус', 'pass', `${gpuLength} мм ≤ ${pcCase.norm.caseGpuMaxMm} мм.`);
  }

  // PSU length
  if (!psu || !pcCase) {
    add('psu-length', 'Длина БП ↔ корпус', 'unknown', 'Нужны БП и корпус.');
  } else if (!psuLength || !pcCase.norm.casePsuMaxMm) {
    add('psu-length', 'Длина БП ↔ корпус', 'unknown', 'Введите длину БП или лимит корпуса вручную.', 'БП ↔ корпус', true);
  } else if (psuLength > pcCase.norm.casePsuMaxMm) {
    add('psu-length', 'Длина БП ↔ корпус', 'fail', `${psuLength} мм при лимите ${pcCase.norm.casePsuMaxMm} мм.`, 'БП ↔ корпус');
  } else {
    add('psu-length', 'Длина БП ↔ корпус', 'pass', `${psuLength} мм ≤ ${pcCase.norm.casePsuMaxMm} мм.`);
  }

  // Power
  const cpuPower = cpu?.norm.tdpW || 0;
  const gpuPower = gpu?.norm.tdpW || 0;
  const estimatedPower = cpuPower || gpuPower ? cpuPower + gpuPower + 100 : null;

  if (!psu || !estimatedPower) {
    add('power', 'Мощность БП', 'unknown', 'Нужны TDP CPU, TBP GPU и мощность БП.');
  } else {
    const headroom = psu.norm.psuW / estimatedPower;
    if (headroom < 1.1) {
      add('power', 'Мощность БП', 'fail', `Оценка ${estimatedPower} W, БП ${psu.norm.psuW} W — запас ${headroom.toFixed(2)}×.`, 'питание');
    } else if (headroom < 1.25) {
      add('power', 'Мощность БП', 'warn', `Оценка ${estimatedPower} W, БП ${psu.norm.psuW} W — запас ${headroom.toFixed(2)}×.`, 'питание');
    } else {
      add('power', 'Мощность БП', 'pass', `Оценка ${estimatedPower} W, БП ${psu.norm.psuW} W — запас ${headroom.toFixed(2)}×.`);
    }

    if (gpuPower >= 250 && !psu.norm.psuAtx3) {
      add('atx3', 'ATX 3.x для transient spikes', 'warn', `GPU ${gpuPower} W, БП без ATX 3.0/3.1.`, 'питание');
    } else if (gpuPower >= 250) {
      add('atx3', 'ATX 3.x для transient spikes', 'pass', 'БП соответствует ATX 3.x.');
    } else {
      add('atx3', 'ATX 3.x для transient spikes', 'pass', 'Для этой GPU не требуется.');
    }
  }

  // GPU power connectors
  if (!gpu || !psu) {
    add('connectors', 'Разъёмы питания GPU', 'unknown', 'Нужны GPU и БП.');
  } else {
    const need = gpu.norm.connectors;
    const have8 = psu.norm.psu8pin;
    if (!need || (!need.eight && !need.twelve)) {
      add('connectors', 'Разъёмы питания GPU', 'unknown', 'В карточке GPU не указан разъём питания.', 'GPU ↔ БП', true);
    } else if (have8 === null && !psu.norm.psu12v) {
      add('connectors', 'Разъёмы питания GPU', 'unknown', 'В карточке БП не указаны разъёмы PCIe. Проверьте кабели вручную.', 'GPU ↔ БП', true);
    } else if (need.twelve && !psu.norm.psu12v) {
      add(
        'connectors',
        'Разъёмы питания GPU',
        need.alternative ? 'warn' : 'fail',
        `GPU: ${need.twelve ? '12V-2x6' : ''}${need.eight ? ` ${need.eight}× 8-pin` : ''}. БП: ${have8}× 8-pin${psu.norm.psu12v ? ', 12V-2x6' : ', без 12V-2x6'}.`,
        'GPU ↔ БП'
      );
    } else if (need.eight > (have8 ?? 0)) {
      add(
        'connectors',
        'Разъёмы питания GPU',
        psu.norm.psu12v ? 'warn' : 'fail',
        `GPU нужно ${need.eight}× 8-pin, у БП ${have8 ?? 0}${psu.norm.psu12v ? ' + 12V-2x6' : ''}.`,
        'GPU ↔ БП'
      );
    } else {
      add('connectors', 'Разъёмы питания GPU', 'pass', `8-pin: ${need.eight}/${have8 ?? 0}${psu.norm.psu12v ? ', 12V-2x6 есть' : ''}.`);
    }
  }

  // Cooler TDP
  if (!cpu || !cooling) {
    add('cooler-tdp', 'TDP кулера ↔ TDP CPU', 'unknown', 'Нужны CPU и охлаждение.');
  } else if (!cooling.norm.coolerTdp || !cpu.norm.tdpW) {
    add('cooler-tdp', 'TDP кулера ↔ TDP CPU', 'unknown', 'Нет TDP-рейтинга кулера.', 'CPU ↔ охлаждение', true);
  } else if (cooling.norm.coolerTdp < cpu.norm.tdpW) {
    add('cooler-tdp', 'TDP кулера ↔ TDP CPU', 'warn', `Кулер ${cooling.norm.coolerTdp} W, CPU ${cpu.norm.tdpW} W.`, 'CPU ↔ охлаждение');
  } else {
    add('cooler-tdp', 'TDP кулера ↔ TDP CPU', 'pass', `${cooling.norm.coolerTdp} W ≥ ${cpu.norm.tdpW} W.`);
  }

  // Bifurcation / M.2
  if (!motherboard) {
    add('bifurcation', 'Линии PCIe / M.2', 'unknown', 'Нужна материнская плата.');
  } else if (motherboard.norm.mbBifurcation) {
    add('bifurcation', 'Линии PCIe / M.2', 'warn', 'Плата может делить линии GPU и M.2. Проверьте схему слотов.', 'плата');
  } else {
    add('bifurcation', 'Линии PCIe / M.2', 'pass', 'Явного риска бифуркации в карточке нет.');
  }

  // Profiles
  const profileResult = profileConflicts(selection, intentId);
  if (!intentId) {
    add('profiles', 'Профили под интент', 'unknown', 'Интент не выбран.');
  } else if (profileResult.conflicts.length) {
    const worst = profileResult.conflicts.some((item) => item.severity === 'fail') ? 'fail' : 'warn';
    add('profiles', 'Профили под интент', worst, `${profileResult.conflicts.length} конфликт(ов), optimal: ${profileResult.optimal}.`, 'профили');
  } else if (profileResult.checked && profileResult.optimal === 0) {
    add('profiles', 'Профили под интент', 'warn', `Нет ни одного optimal-профиля для ${intentId}.`, 'профили');
  } else {
    add('profiles', 'Профили под интент', 'pass', `optimal: ${profileResult.optimal}, проверено карточек: ${profileResult.checked}.`);
  }

  // Budget
  let total = 0;
  let priced = 0;
  for (const key of REQUIRED) {
    const component = parts[key];
    if (component?.price) {
      total += component.price;
      priced += 1;
    }
  }

  if (budget && total > budget) {
    add('budget', 'Бюджет', 'warn', `${new Intl.NumberFormat('ru-RU').format(total)} ₽ при потолке ${new Intl.NumberFormat('ru-RU').format(budget)} ₽.`);
  } else if (budget) {
    add('budget', 'Бюджет', 'pass', `${new Intl.NumberFormat('ru-RU').format(total)} ₽ ≤ ${new Intl.NumberFormat('ru-RU').format(budget)} ₽.`);
  } else {
    add('budget', 'Бюджет', 'unknown', 'Бюджет не задан.');
  }

  // Data completeness
  const missingFields = [];
  let totalFields = 0;
  let knownFields = 0;
  for (const key of REQUIRED) {
    const component = parts[key];
    if (!component) continue;
    for (const [field, label] of FIELD_RULES[key] || []) {
      totalFields += 1;
      let value = component.norm[field];
      if (field === 'gpuLengthMm') value = measurement(measurements, 'gpuLengthMm', value);
      if (field === 'coolerHeightMm') value = measurement(measurements, 'coolerHeightMm', value) || component.norm.radiatorMm;
      if (field === 'ramHeightMm') value = measurement(measurements, 'ramHeightMm', value);
      if (isKnown(value, field)) knownFields += 1;
      else missingFields.push(`${component.title}: ${label}`);
    }
  }
  const completeness = {
    total: totalFields,
    known: knownFields,
    score: totalFields ? Math.round((knownFields / totalFields) * 100) : 0,
    missing: missingFields
  };
  add(
    'data',
    'Полнота данных',
    completeness.score === 100 ? 'pass' : 'unknown',
    `${knownFields}/${totalFields} полей (${completeness.score}%).${missingFields.length ? ' Не хватает: ' + missingFields.slice(0, 4).join(', ') + (missingFields.length > 4 ? '…' : '') : ''}`
  );

  // Issues for the UI: fail/warn checks + critical unknowns.
  const issues = checks
    .filter((check) => check.status === 'fail' || check.status === 'warn')
    .map((check) => ({
      severity: check.status,
      component: check.component,
      title: check.label,
      detail: check.detail
    }));

  for (const check of checks) {
    if (check.status === 'unknown' && check.critical) {
      issues.push({
        severity: 'info',
        component: check.component,
        title: `${check.label}: нет данных`,
        detail: check.detail
      });
    }
  }

  issues.sort((a, b) => (STATUS_ORDER[a.severity] ?? 9) - (STATUS_ORDER[b.severity] ?? 9));

  const hasFail = checks.some((check) => check.status === 'fail');
  const hasWarn = checks.some((check) => check.status === 'warn');
  const hasCriticalUnknown = checks.some((check) => check.status === 'unknown' && check.critical);
  const status = hasFail ? 'FAIL' : hasWarn || hasCriticalUnknown ? 'WARN' : 'PASS';

  const bom = BUILD_CATEGORIES.map((category) => ({
    key: category.key,
    label: category.label,
    component: parts[category.key]
  })).filter((item) => item.component);

  return {
    status,
    issues,
    checks,
    total,
    priced,
    missing,
    estimatedPower,
    optimalCount: profileResult.optimal,
    profiledCount: profileResult.checked,
    completeness,
    bom,
    measurements: {
      gpuLengthMm: gpuLength,
      coolerHeightMm: coolerHeight,
      psuLengthMm: psuLength,
      ramHeightMm: ramHeight
    }
  };
}

export function validateBuild(selection, intentId, budget = null) {
  return assessBuild(selection, intentId, budget);
}

export function encodeBuild(selection, intentId, budget, measurements = {}) {
  const params = new URLSearchParams();
  for (const key of REQUIRED) {
    if (selection[key]) params.set(key, selection[key]);
  }
  if (intentId) params.set('intent', intentId);
  if (budget) params.set('budget', String(budget));
  for (const [key, value] of Object.entries(measurements)) {
    if (value !== '' && value !== null && value !== undefined) params.set(`m_${key}`, String(value));
  }
  return params.toString();
}

export function decodeBuild(search) {
  const params = new URLSearchParams(search);
  const selection = {};
  for (const key of REQUIRED) {
    const value = params.get(key);
    if (value && bySlug.has(value)) selection[key] = value;
  }
  const measurements = {};
  for (const key of ['gpuLengthMm', 'coolerHeightMm', 'psuLengthMm', 'ramHeightMm']) {
    const value = params.get(`m_${key}`);
    if (value) measurements[key] = Number(value);
  }
  return {
    selection,
    intentId: params.get('intent') || 'aaa_1440p_high',
    budget: Number(params.get('budget')) || 150000,
    measurements
  };
}

export const STATUS_TEXT = {
  PASS: 'ПРОЙДЕНО',
  WARN: 'ЕСТЬ ЗАМЕЧАНИЯ',
  FAIL: 'НЕСОВМЕСТИМО'
};
