const apiKey = '38212142fbabe3881e01dcbb9527c88b'; // TMDb'den aldığınız API anahtarını buraya ekleyin
const url = 'https://api.themoviedb.org/3/tv/top_rated'; // TMDb Top Rated TV Shows API URL

// API'den en çok oy alan dizileri çeken fonksiyon
async function fetchTopRatedTVShows() {
    try {
        const response = await fetch(`${url}?api_key=${apiKey}&language=en-US&page=1`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error('Failed to fetch top-rated TV shows');
        }

        const data = await response.json();
        displayTopRatedTVShows(data.results);
    } catch (error) {
        console.error('Error fetching top-rated TV shows:', error);
        document.getElementById('directorGrid').innerHTML = '<p>Failed to load top-rated TV shows. Please try again later.</p>';
    }
}

// Ekranda en çok oy alan dizileri listelemek için bir fonksiyon
function displayTopRatedTVShows(shows) {
    const directorGrid = document.getElementById('directorGrid');
    directorGrid.innerHTML = ''; // Önceki içerikleri temizle

    shows.forEach(show => {
        const showCard = document.createElement('div');
        showCard.classList.add('director-card');

        showCard.innerHTML = `
            <img src="https://image.tmdb.org/t/p/w500${show.poster_path}" alt="${show.name}">
            <h3>${show.name}</h3>
            <p>Rating: ${show.vote_average}</p>
            <p>${show.overview.slice(0, 100)}...</p>
        `;

        directorGrid.appendChild(showCard);
    });
}

// Sayfa yüklendiğinde en çok oy alan dizileri çek
window.onload = fetchTopRatedTVShows;
