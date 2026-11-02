(() => {
  document.querySelector('#print').addEventListener('click', () => window.print());
  if (!('IntersectionObserver' in window)) return;
  const links = [...document.querySelectorAll('.sidebar a')];
  const observer = new IntersectionObserver(entries => {
    const first = entries.filter(x => x.isIntersecting).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
    if (!first) return;
    links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + first.target.id));
  }, {rootMargin:'-5% 0px -65% 0px', threshold:0});
  document.querySelectorAll('.insight-topic, #pipeline').forEach(n => observer.observe(n));
})();
