function Matrix(length) {
    var arr = new Array(length || 0),
        i = length;

    if (arguments.length > 1) {
        var args = Array.prototype.slice.call(arguments, 1);
        while (i--) arr[length - 1 - i] = Matrix.apply(this, args);
    }

    return arr;
}



battlefield = Matrix(10, 10)


ship = { length: 4, cordinates: [[1, 2][4, 2]] }

function tableCreate() {
    var body = document.body,
        tbl = document.createElement('table');
    tbl.style.width = '100px';
    tbl.style.border = '1px solid black';

    for (var i = 0; i < battlefield.length; i++) {
        var tr = tbl.insertRow();
        for (var j = 0; j < battlefield[0].length; j++) {
            var td = tr.insertCell();
            td.appendChild(document.createTextNode(`${i}:${j}`));
            td.style.border = '1px solid black';
            td.id = `${i}:${j}`
            td.onclick = function(e){click_test(e.target.textContent)}
        }
    }
    body.appendChild(tbl);
}
tableCreate();

document.querySelectorAll('td')


function click_test(xy) {
    console.log('This is')
    console.log(xy)
}


function tableUpdate() {

}