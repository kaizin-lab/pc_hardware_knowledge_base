<script>
  import '../app.css';
  import { base } from '$app/paths';
  let { children } = $props();
</script>

<div class="bg-grid"></div>

<header class="topbar">
  <a class="brand" href="{base}/">
    <span class="brand-mark">P</span>
    <span class="brand-name">PCBO KB</span>
    <span class="brand-sub">Hardware Knowledge Base</span>
  </a>
  <nav class="nav">
    <a href="{base}/catalog/">Каталог</a>
    <a href="{base}/build/">Сборка</a>
    <a class="cta" href="https://github.com/kaizin-lab/pc_hardware_knowledge_base" rel="noreferrer">GitHub</a>
  </nav>
</header>

<main class="shell">
  {@render children()}
</main>

<footer class="footer">
  <span>PC Hardware Knowledge Base</span>
  <span class="footer-sep">/</span>
  <a href="{base}/catalog/">каталог</a>
  <span class="footer-sep">/</span>
  <a href="{base}/build/">конструктор</a>
  <span class="footer-sep">/</span>
  <span>данные из Markdown + YAML</span>
</footer>
