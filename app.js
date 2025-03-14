const carouselContainer = document.getElementById('carouselContainer');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

let currentIndex = 0; 
let movies = [];

const apiKey = '38212142fbabe3881e01dcbb9527c88b';
const baseUrl = 'https://api.themoviedb.org/3';
const nowPlayingUrl = `${baseUrl}/movie/now_playing?api_key=${apiKey}&language=en-US&page=1`;

const fetchMovies = async () => {
    try {
        const response = await fetch(nowPlayingUrl);
        const data = await response.json();
        movies = data.results; 
        renderMovies(); 
    } catch (error) {
        console.error('Error fetching movies:', error);
    }
};

const renderMovies = () => {
    carouselContainer.innerHTML = ''; 

    movies.forEach((movie) => {
        if (movie.poster_path) { 
            const movieImage = document.createElement('img');
            movieImage.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
            movieImage.alt = movie.title;
            movieImage.classList.add('carousel-item'); 
            carouselContainer.appendChild(movieImage);
        }
    });
};

const moveToNext = () => {
    if (currentIndex < movies.length - 3) { 
        currentIndex++;
        updateCarouselPosition();
    }
};

const moveToPrev = () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateCarouselPosition();
    }
};

const updateCarouselPosition = () => {
    const offset = -currentIndex * 270; 
    carouselContainer.style.transform = `translateX(${offset}px)`;
};

nextBtn.addEventListener('click', moveToNext);
prevBtn.addEventListener('click', moveToPrev);

fetchMovies();
