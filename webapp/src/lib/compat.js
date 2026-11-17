import { BUILD_CATEGORIES, bySlug } from './kb.js';

const REQUIRED = BUILD_CATEGORIES.map((category) => category.key);

function issue(severity, component, title, detail) {
  return { severity, component, title, detail };
}

function selectedComponents(selection) {
  const result = {};
  for (const key of REQUIRED) {
    result[key] = selection[key] ? bySlug.get(selection[key]) : null;
  }
  return result;
}

function profileIssues(selection, intentId, issues) {
  if (!intentId) return { optimal: 0, checked: 0 };

  let optimal = 0;
  let checked = 0;

  for (const key of REQUIRED) {
    const component = bySlug.get(selection[key]);
    if (!component || !component.profiles.length) continue;
    checked += 1;

    for (const profile of component.profiles) {
      if (profile.optimal.includes(intentId)) optimal += 1;
      if (profile.failure.includes(intentId)) {
        issues.push(
          issue(
            profile.severity === 'BLOCK' ? 'fail' : 'warn',
            component.title,
            `Профиль ${profile.name}`,
            profile.failureMode || `Компонент не оптимален для интента ${intentId}.`
          )
        );
      }
    }
  }

  return { optimal, checked };
}

export function validateBuild(selection, intentId, budget = null) {
  const issues = [];
  const parts = selectedComponents(selection);

  const missing = REQUIRED.filter((key) => !parts[key]);
  if (missing.length) {
    const labels = missing
      .map((key) => BUILD_CATEGORIES.find((category) => category.key === key)?.label || key)
      .join(', ');
    issues.push(
      issue('warn', 'Сборка', 'Не хватает компонентов', `Не выбрано: ${labels}. Проверка неполная.`)
    );
  }

  const cpu = parts.cpu;
  const motherboard = parts.motherboard;
  const gpu = parts.gpu;
  const memory = parts.memory;
  const psu = parts.psu;
  const cooling = parts.cooling;
  const pcCase = parts.case;

  if (cpu?.norm.socket && motherboard?.norm.socket && cpu.norm.socket !== motherboard.norm.socket) {
    issues.push(
      issue(
        'fail',
        'CPU ↔ плата',
        'Сокет не совпадает',
        `${cpu.title}: ${cpu.norm.socket}; ${motherboard.title}: ${motherboard.norm.socket}.`
      )
    );
  }

  const memoryPairs = [
    ['CPU ↔ память', cpu, memory],
    ['плата ↔ память', motherboard, memory]
  ];
  for (const [label, left, right] of memoryPairs) {
    if (left?.norm.memoryType && right?.norm.memoryType && left.norm.memoryType !== right.norm.memoryType) {
      issues.push(
        issue(
          'fail',
          label,
          'Тип памяти не совпадает',
          `${left.title}: ${left.norm.memoryType}; ${right.title}: ${right.norm.memoryType}.`
        )
      );
    }
  }

  if (motherboard?.norm.formFactor && pcCase?.norm.caseForms.length) {
    const supported = pcCase.norm.caseForms;
    if (!supported.includes(motherboard.norm.formFactor)) {
      issues.push(
        issue(
          'fail',
          'плата ↔ корпус',
          'Форм-фактор не поддерживается',
          `${motherboard.title}: ${motherboard.norm.formFactor}; корпус: ${supported.join(', ')}.`
        )
      );
    }
  }

  if (cpu?.norm.socket && cooling?.norm.sockets.length) {
    if (!cooling.norm.sockets.includes(cpu.norm.socket)) {
      issues.push(
        issue(
          'fail',
          'CPU ↔ охлаждение',
          'Кулер не поддерживает сокет',
          `${cooling.title}: ${cooling.norm.sockets.join(', ')}; нужен ${cpu.norm.socket}.`
        )
      );
    }
  }

  if (cooling?.norm.coolerHeightMm && pcCase?.norm.caseCoolerMaxMm) {
    if (cooling.norm.coolerHeightMm > pcCase.norm.caseCoolerMaxMm) {
      issues.push(
        issue(
          'fail',
          'охлаждение ↔ корпус',
          'Кулер не влезает по высоте',
          `${cooling.norm.coolerHeightMm} мм при лимите ${pcCase.norm.caseCoolerMaxMm} мм.`
        )
      );
    }
  }

  if (gpu?.norm.gpuLengthMm && pcCase?.norm.caseGpuMaxMm && gpu.norm.gpuLengthMm > pcCase.norm.caseGpuMaxMm) {
    issues.push(
      issue(
        'fail',
        'GPU ↔ корпус',
        'Видеокарта не влезает',
        `${gpu.norm.gpuLengthMm} мм при лимите ${pcCase.norm.caseGpuMaxMm} мм.`
      )
    );
  }

  const cpuPower = cpu?.norm.tdpW || 0;
  const gpuPower = gpu?.norm.tdpW || 0;
  const estimatedPower = cpuPower || gpuPower ? cpuPower + gpuPower + 100 : null;

  if (psu?.norm.psuW && estimatedPower) {
    const headroom = psu.norm.psuW / estimatedPower;
    if (headroom < 1.1) {
      issues.push(
        issue(
          'fail',
          'питание',
          'Блока питания недостаточно',
          `Оценка нагрузки ${estimatedPower} W, БП ${psu.norm.psuW} W — запас ${headroom.toFixed(2)}×.`
        )
      );
    } else if (headroom < 1.25) {
      issues.push(
        issue(
          'warn',
          'питание',
          'Маленький запас по мощности',
          `Оценка нагрузки ${estimatedPower} W, БП ${psu.norm.psuW} W — запас ${headroom.toFixed(2)}×.`
        )
      );
    }

    if (gpuPower >= 250 && !psu.norm.psuAtx3) {
      issues.push(
        issue(
          'warn',
          'питание',
          'Нет ATX 3.x под transient spikes',
          `GPU ${gpuPower} W. Для пиковых нагрузок лучше БП ATX 3.0/3.1.`
        )
      );
    }
  }

  if (!gpu?.norm.gpuLengthMm && gpu && pcCase) {
    issues.push(
      issue(
        'info',
        'GPU ↔ корпус',
        'Длина GPU не заведена в карточку',
        'Проверьте клиренс корпуса вручную: в базе нет поля длины видеокарты.'
      )
    );
  }

  const profileResult = profileIssues(selection, intentId, issues);
  if (intentId && profileResult.checked > 0 && profileResult.optimal === 0) {
    issues.push(
      issue(
        'warn',
        'профили',
        'Нет ни одного optimal-профиля',
        `Ни один выбранный компонент не помечен как optimal для ${intentId}.`
      )
    );
  }

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
    issues.push(
      issue(
        'warn',
        'бюджет',
        'Бюджет превышен',
        `${new Intl.NumberFormat('ru-RU').format(total)} ₽ при потолке ${new Intl.NumberFormat('ru-RU').format(budget)} ₽.`
      )
    );
  }

  const order = { fail: 0, warn: 1, info: 2 };
  issues.sort((a, b) => order[a.severity] - order[b.severity]);

  const status = issues.some((item) => item.severity === 'fail')
    ? 'FAIL'
    : issues.some((item) => item.severity === 'warn')
      ? 'WARN'
      : 'PASS';

  return {
    status,
    issues,
    total,
    priced,
    missing,
    estimatedPower,
    optimalCount: profileResult.optimal,
    profiledCount: profileResult.checked
  };
}

export const STATUS_TEXT = {
  PASS: 'ПРОЙДЕНО',
  WARN: 'ЕСТЬ ЗАМЕЧАНИЯ',
  FAIL: 'НЕСОВМЕСТИМО'
};
