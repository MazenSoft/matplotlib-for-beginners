const navItems = document.querySelectorAll(".nav-item");  
const contents = document.querySelectorAll('.show-content');  

// Function to show content and manage active state  
function showContent(contentId) {  
    // Hide all contents  
    contents.forEach(content => {  
        content.style.display = 'none';  
    });  

    // Show the requested content  
    document.getElementById(contentId).style.display = 'block';  
    
    // Update the active nav item  
    updateActiveNav(contentId);  
}  

// Function to update the active class based on the clicked item  
function updateActiveNav(contentId) {  
    navItems.forEach((navItem) => {  
        const onclickValue = navItem.getAttribute('onclick');  
        if (onclickValue && onclickValue.includes(contentId)) {  
            navItem.classList.add('active');  
        } else {  
            navItem.classList.remove('active');  
        }  
    });  
}  

// Listener for the links in the content box  
const contenerStyles = document.querySelectorAll('.contener-style');  

contenerStyles.forEach((style) => {  
    style.addEventListener("click", () => {  
        const contentId = style.onclick.toString().match(/'([^']+)'/)[1];  
        showContent(contentId);  
    });  
});  

// Show Home content and set it as active on page load  
window.onload = function() {  
    showContent('home'); // Show home on load  
};