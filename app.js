// Element seçiciler
const carouselContainer = document.getElementById('carouselContainer');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

let currentIndex = 0; // Kaydırıcıdaki başlangıç index'i
let movies = []; // Filmleri saklamak için boş dizi

// TheMovieDB API bilgileri
const apiKey = '38212142fbabe3881e01dcbb9527c88b'; // Buraya kendi API anahtarınızı ekleyin
const baseUrl = 'https://api.themoviedb.org/3';
const nowPlayingUrl = `${baseUrl}/movie/now_playing?api_key=${apiKey}&language=en-US&page=1`;

// API'den gösterimde olan filmleri alma fonksiyonu
const fetchMovies = async () => {
    try {
        const response = await fetch(nowPlayingUrl);
        const data = await response.json();
        movies = data.results; // Filmler listesi
        renderMovies(); // Filmleri ekrana yerleştir
    } catch (error) {
        console.error('Error fetching movies:', error);
    }
};

// Filmleri kaydırıcıya ekleyen fonksiyon
const renderMovies = () => {
    carouselContainer.innerHTML = ''; // Önceki içerikleri temizle

    movies.forEach((movie) => {
        if (movie.poster_path) { // Poster varsa ekle
            const movieImage = document.createElement('img');
            movieImage.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
            movieImage.alt = movie.title;
            movieImage.classList.add('carousel-item'); // Stil için sınıf ekle
            carouselContainer.appendChild(movieImage);
        }
    });
};

// Kaydırıcıyı sağa kaydırma fonksiyonu
const moveToNext = () => {
    if (currentIndex < movies.length - 3) { // Ekranda 3 film görünecek
        currentIndex++;
        updateCarouselPosition();
    }
};

// Kaydırıcıyı sola kaydırma fonksiyonu
const moveToPrev = () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateCarouselPosition();
    }
};

// Kaydırıcıyı güncelleme fonksiyonu
const updateCarouselPosition = () => {
    const offset = -currentIndex * 270; // Her filmin genişliği + margin 270px
    carouselContainer.style.transform = `translateX(${offset}px)`;
};

// Olay dinleyicileri
nextBtn.addEventListener('click', moveToNext);
prevBtn.addEventListener('click', moveToPrev);

// Sayfa yüklendiğinde filmleri çek
fetchMovies();
