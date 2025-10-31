// Publications filtering functionality

document.addEventListener('DOMContentLoaded', function() {
    const yearFilter = document.getElementById('year-filter');
    const publicationsContainer = document.getElementById('publications-container');
    
    if (yearFilter && publicationsContainer) {
        yearFilter.addEventListener('change', function() {
            const selectedYear = this.value;
            const publications = publicationsContainer.querySelectorAll('.publication');
            const noResults = publicationsContainer.querySelector('.no-results');
            let visibleCount = 0;
            
            publications.forEach(pub => {
                const pubYear = pub.getAttribute('data-year');
                
                if (selectedYear === 'all') {
                    pub.style.display = 'block';
                    visibleCount++;
                } else if (selectedYear === 'older') {
                    const year = parseInt(pubYear);
                    if (year < 2021) {
                        pub.style.display = 'block';
                        visibleCount++;
                    } else {
                        pub.style.display = 'none';
                    }
                } else if (pubYear === selectedYear) {
                    pub.style.display = 'block';
                    visibleCount++;
                } else {
                    pub.style.display = 'none';
                }
            });
            
            // Show/hide "no results" message
            if (noResults) {
                if (visibleCount === 0) {
                    noResults.style.display = 'block';
                } else {
                    noResults.style.display = 'none';
                }
            }
        });
    }
});
