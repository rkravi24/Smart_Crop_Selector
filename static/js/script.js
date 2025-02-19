document.addEventListener("DOMContentLoaded", function () {
    console.log("JS file loaded!");

    const weather = document.getElementById('weather');
    const arrow = document.getElementById('arrow');
    const input = document.getElementById('cityInput');

    arrow.addEventListener("click", () => { 
        event.preventDefault();         // why ? 
                                        // Arrow button was inside a <form>, and when clicked it:
                                        // The browser automatically submitted the form.
                                        // This caused the page to refresh.
                                        // JavaScript stopped running before it could fetch the API.
        const city = input.value.trim();
        if (city) {
            console.log("Fetching weather for:", city);
            fetchWeather(city);
        } else {
            alert("Enter city name!");
        }
    });

    async function fetchWeather(city) {
        const apiKey = '08c0db4c05210810ab58554e877f4372';
        const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
        
        console.log("Fetching from:", apiUrl);


        try {
            const response = await fetch(apiUrl);
            const data = await response.json();

            if (data.cod === 200) {
                const temperature = data.main.temp;
                const precipitation = data.rain ? data.rain['1h'] || 0 : 0;
                const humidity = data.main.humidity;
                const windSpeed = data.wind.speed;

                const weatherInfo = `${temperature} °C | Precipitation: ${precipitation} mm | Humidity: ${humidity}% | Wind: ${windSpeed} m/s`;
                console.log(weatherInfo);
                weather.innerText = weatherInfo;
            } else {
                console.error('Error fetching weather data:', data.message);
                weather.innerText = "Error: " + data.message;
            }
        } catch (error) {
            console.error('Error fetching weather data:', error);
            weather.innerText = "Error fetching data.";
        }
    }

});
