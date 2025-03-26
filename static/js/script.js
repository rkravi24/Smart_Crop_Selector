document.addEventListener("DOMContentLoaded", async function () {
    console.log("JS file loaded!");

    // Check if this is a reload using the Performance API
    const navType = performance.getEntriesByType("navigation")[0]?.type;

    if (navType === "reload") {
        console.log("Page reloaded. Clearing weather data.");
        sessionStorage.removeItem("weatherCity");
        sessionStorage.removeItem("weatherData");
    }

    const weather = document.getElementById('weather');
    const arrow = document.getElementById('arrow');
    const input = document.getElementById('cityInput');


        let apiKey = null;

        // Load API Key Securely from Flask
        async function loadApiKey() {
            try {
                const response = await fetch("/get-js-api-key");
                const data = await response.json();
                apiKey = data.js_api_key;
                console.log("API Key Loaded Securely:", apiKey);
            } catch (error) {
                console.error("Error fetching API Key:", error);
            }
        }

        // Load API key before making API requests
        await loadApiKey();


    if (sessionStorage.getItem("weatherCity") && sessionStorage.getItem("weatherData")) {
        input.value = sessionStorage.getItem("weatherCity");
        weather.innerText = sessionStorage.getItem("weatherData");
    }

    arrow.addEventListener("click", (event) => { 
        event.preventDefault();         // why ? 
                                        // Arrow button was inside a <form>, and when clicked it:
                                        // The browser automatically submitted the form.
                                        // This caused the page to refresh.
                                        // JavaScript stopped running before it could fetch the API.
        const city = input.value.trim();
        if (city) {
            if(sessionStorage.getItem("weatherCity")!== city){
                console.log("Fetching weather for:", city);
                fetchWeather(city);
            }
        } else {
            alert("Enter city name!");
        }
    });

    async function fetchWeather(city) {
           if (!apiKey) {
                console.error("API Key not loaded. Cannot fetch weather.");
                return;
            }
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
                sessionStorage.setItem("weatherCity", city);
                sessionStorage.setItem("weatherData", weatherInfo);
                
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