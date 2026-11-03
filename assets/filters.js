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

  var tags = Object.keys(tagSet).sort(function (a, b) {
    return a.localeCompare(b, undefined, { sensitivity: 'base' });
  });

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

  // Show the year label only on the first visible entry of each year, so a
  // year never loses its label when its first entry is filtered out.
  function regroupYears() {
    timelines.forEach(function (timeline) {
      var prev = null;
      timeline.querySelectorAll('.pub-tl-item[data-year]').forEach(function (el) {
        if (el.style.display === 'none') return;
        var year = el.dataset.year;
        var same = year === prev;
        prev = year;
        el.classList.toggle('same-year', same);
        var label = el.querySelector('.pub-tl-year');
        if (label) label.textContent = same ? '' : year;
      });
    });
  }

  function filterPubs(selectedTag) {
    allItems.forEach(function (item) {
      if (!selectedTag || item.tags.indexOf(selectedTag) !== -1) {
        item.el.style.display = '';
      } else {
        item.el.style.display = 'none';
      }
    });
    regroupYears();

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
