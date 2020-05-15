function setActiveCategory(selection) {
    var x = document.getElementById("category-menu-items").querySelectorAll(".list-inline-item a");
    for (let i = 0; i < x.length; i++) {
        x[i].style.color = 'rgb(123, 123, 123)';
    }
    document.getElementById(selection).style.color = 'rgb(181, 95, 95)';
}