let crbtn = document.getElementById("Content Writer");
console.log(crbtn)
let hrbtn = document.getElementById("HR");
console.log(hrbtn)
let seobtn = document.getElementById("SEO");
console.log(hrbtn)
let sabtn = document.getElementById("Sales");
console.log(sabtn)
let mangbtn = document.getElementById("Management/Admin");
console.log(mangbtn)
let ddbtn = document.getElementById("Design & Development");
console.log(ddbtn)

let depart = document.getElementById("department")
// console.log(depart.value = crbtn.value) 

cate = document.querySelector(".category")
form = document.querySelector(".wrapper")


crbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = crbtn.value
    form.classList.remove('wrapper-visibility')

})

hrbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = hrbtn.value
    form.classList.remove('wrapper-visibility')

})

sabtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = sabtn.value
    form.classList.remove('wrapper-visibility')

})

mangbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = mangbtn.value
    form.classList.remove('wrapper-visibility')

})

seobtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = seobtn.value
    form.classList.remove('wrapper-visibility')

})
ddbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = ddbtn.value
    form.classList.remove('wrapper-visibility')

})


let counter = 0;

function startCounter() {
    setInterval(() => {
        counter++;
        updatePopupContent(counter);
    }, 1000);  // Update every second (1000 milliseconds)
}

function updatePopupContent(value) {
    // Update the popup content with the counter value
    document.getElementById('counter-popup').innerText = value;
}