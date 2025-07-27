// Global variable to store all stocks
let allStocks = [];

// Load all stocks when page loads
async function loadAllStocks() {
        const response = await fetch('/api/all-stocks');
        allStocks = await response.json();
}

// Filter stocks based on user input
function filterStocks(query) {
    if (query.length < 1) {
        return [];
    } 
    
    const filtered = allStocks.filter(stock => 
        stock.symbol.toLowerCase().startsWith(query.toLowerCase()) ||
        stock.name.toLowerCase().includes(query.toLowerCase())
    );
    
    // Sort to show symbol matches first, limit to 50 results
    return filtered.sort((a, b) => {
            const aSymbolMatch = a.symbol.toLowerCase().startsWith(query.toLowerCase()); // returns boolean b/c of startswith()
            const bSymbolMatch = b.symbol.toLowerCase().startsWith(query.toLowerCase());
            if (aSymbolMatch && !bSymbolMatch) { // a comes first, so move it towards the top of the search bar
                return -1;
            }
            if (!aSymbolMatch && bSymbolMatch) { // b comes first
                return 1;
            }
            return 0; // same priorty, soo just keep the same order
        }).slice(0, 50);
}

// Display suggestions in the dropdown
// the illusion of displaying a dropdown is actually just a li wrapped in ul tags, with some js and css.
function displaySuggestions(suggestions) {
    const suggestionsList = document.getElementById('suggestions');
    suggestionsList.innerHTML = ''; //prevent duplicate by starting with a fresh suggestionList
    
    suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = `${suggestion.symbol} - ${suggestion.name}`; // this will set the visible suggestion as eg: AAPL - Apple Inc.
        li.className = 'suggestion-item'; // for css later
        
        // When user clicks a suggestion
        li.addEventListener('click', () => {
            document.getElementById('stock-search').value = suggestion.symbol; // when the suggestion is clicked, fill the search bar with it
            suggestionsList.innerHTML = ''; // clear the dropdown options
        });
        
        suggestionsList.appendChild(li); // this is just filling the search bar so it actually appears 
    });
}

// Initialize autocomplete when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load all stocks
    loadAllStocks();
    
    // Set up search input listener
    const searchInput = document.getElementById('stock-search'); // just trying to shorten my code a little, so store in a variable
    const suggestionsList = document.getElementById('suggestions');
    
    if (searchInput) {
        searchInput.addEventListener('input', function(e) { // goes off everytime someone types in the search bar
            const query = e.target.value;
            
            if (query.length < 1) {
                suggestionsList.innerHTML = '';
                return;
            }
            
            const suggestions = filterStocks(query);
            displaySuggestions(suggestions);
        });
        
        // Hide suggestions when clicking outside of input box or on the dropdown list
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !suggestionsList.contains(e.target)) {
                suggestionsList.innerHTML = '';
            }
        });
    }
});
// blurs out button, if you haven't searched anything yet.
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('stock-search');
    const button = document.getElementById('check-btn');
    
    input.addEventListener('input', function() {
        if (input.value.trim().length > 0) {
            button.disabled = false;
        } else {
            button.disabled = true;
        }
    });
});