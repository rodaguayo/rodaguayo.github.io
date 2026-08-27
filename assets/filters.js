document.addEventListener('DOMContentLoaded', function () {
  var timelines = document.querySelectorAll('.pub-timeline');
  if (!timelines.length) return;

  var allItems = [];
  var tagSet = {};

  timelines.forEach(function (timeline) {
    var items = timeline.querySelectorAll('.pub-tl-item');
    items.forEach(function (item) {
      var tags = (item.dataset.tags || '').split('|').filter(Boolean);
      tags.forEach(function (t) { tagSet[t] = true; });
      allItems.push({ el: item, tags: tags });
    });
  });

  var tags = Object.keys(tagSet).sort();

  var filterBar = document.createElement('div');
  filterBar.className = 'tag-filter-bar';

  var allBtn = document.createElement('button');
  allBtn.className = 'tag-filter active';
  allBtn.textContent = 'All';
  allBtn.dataset.tag = '';
  filterBar.appendChild(allBtn);

  tags.forEach(function (tag) {
    var btn = document.createElement('button');
    btn.className = 'tag-filter';
    btn.textContent = tag;
    btn.dataset.tag = tag;
    filterBar.appendChild(btn);
  });

  timelines[0].parentNode.insertBefore(filterBar, timelines[0]);

  function filterPubs(selectedTag) {
    allItems.forEach(function (item) {
      if (!selectedTag || item.tags.indexOf(selectedTag) !== -1) {
        item.el.style.display = '';
      } else {
        item.el.style.display = 'none';
      }
    });

    filterBar.querySelectorAll('.tag-filter').forEach(function (btn) {
      if (btn.dataset.tag === selectedTag) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  filterBar.addEventListener('click', function (e) {
    var btn = e.target.closest('.tag-filter');
    if (!btn) return;
    filterPubs(btn.dataset.tag);
  });
});
