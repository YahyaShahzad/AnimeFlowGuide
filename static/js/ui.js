// UI interactions: search, filters, mobile menu
document.addEventListener('DOMContentLoaded', () => {
  const search = document.getElementById('site-search');
  const searchMobile = document.getElementById('site-search-mobile');
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const clearBtn = document.getElementById('search-clear');
  const grid = document.getElementById('anime-grid');
  const resultCount = document.getElementById('result-count');
  const filterType = document.getElementById('filter-type');
  const sortBy = document.getElementById('sort-by');

  function setUp() {
    if (mobileBtn) mobileBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    if (clearBtn && search) clearBtn.addEventListener('click', () => { search.value = ''; filterGrid(); });

    if (search) search.addEventListener('input', filterGrid);
    if (searchMobile) searchMobile.addEventListener('input', filterGrid);
    if (filterType) filterType.addEventListener('change', filterGrid);
    if (sortBy) sortBy.addEventListener('change', sortGrid);
  }

  function filterGrid() {
    if (!grid) return;
    const q = (search ? search.value : '') || (searchMobile ? searchMobile.value : '');
    const type = (filterType ? filterType.value : 'all');
    const items = Array.from(grid.querySelectorAll('article.anime-card'));
    let visible = 0;
    items.forEach(it => {
      const name = (it.dataset.name || '').toLowerCase();
      const slug = (it.dataset.slug || '').toLowerCase();
      const matchQ = q.trim() === '' || name.includes(q.toLowerCase()) || slug.includes(q.toLowerCase());
      const matchType = (type === 'all') || (type === 'canon' && it.dataset.name.toLowerCase().includes('naruto')) || true; // placeholder logic
      if (matchQ && matchType) { it.style.display = ''; visible++; } else { it.style.display = 'none'; }
    });
    if (resultCount) resultCount.textContent = visible;
  }

  function sortGrid() {
    if (!grid) return;
    const v = sortBy.value;
    const items = Array.from(grid.querySelectorAll('article.anime-card'));
    const sorted = items.sort((a,b)=>{
      if (v === 'name') return a.dataset.name.localeCompare(b.dataset.name);
      return 0;
    });
    sorted.forEach(el => grid.appendChild(el));
  }

  setUp();
  filterGrid();
});