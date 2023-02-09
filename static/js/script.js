// Scroll to the Top of the page refresh
// if (history.scrollRestoration) {
//   history.scrollRestoration = "manual";
// } else {
//   window.onbeforeunload = function () {
//     window.scrollTo(0, 0);
//   };
// }

if (history.replaceState) {
    history.replaceState(null, null, location.href);
}

// csrftoken cookie 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Side Alert



// const dataContainer = document.querySelector('[data-container]')
// const dataTemplate = document.querySelector('[data-template]')
// const dataTags = document.querySelector('[data-tags]')
// const dataMessage = document.querySelector('[data-message]')

// const createSideAlert = (message) => {
//     // Clone tghe template
//     element = dataTemplate.cloneNode(true)

//    // Remove the data-template attribute
//     delete element.dataset.dataTemplate

//     // Set the text
//     dataMessage.innerHTML = message.message
//     dataTags.innerHTML = message.tags

//     // Add the new element to the container
//     dataContainer.appendChild(element)
// }

// let showAlert = false

// document.body.addEventListener("messages", function(e){
//     // alert(evt.detail);  
//     console.log(e.detail.value[0]);
//     e.detail.value.forEach(createSideAlert)
//     showAlert = true
// })

  