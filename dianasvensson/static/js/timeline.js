const timelineItems = document.querySelectorAll('.timeline-fade-in');

function handleIntersection(entries, observer) {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('visible');
        const h4 = entry.target.querySelector('h4');
        if (h4) {
          h4.classList.add('highlight');
        }
      }, index * 300); // Delay each item by 300ms
    }
  });
}

const options = {
  rootMargin: '0px',
  threshold: 0.3,
};

const observer = new IntersectionObserver(handleIntersection, options);

timelineItems.forEach(item => {
  observer.observe(item);
});

