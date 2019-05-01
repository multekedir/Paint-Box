let request = new XMLHttpRequest();

request.onload = function () {
    let data = this.response;
    if (request.status >= 200 && request.status < 400) {
            console.log(data)

    } else {
        console.log('error')
    }
};

function del(id) {
    request.open('POST', 'http://127.0.0.1:5000/del_project/0', true);
    request.send();
}





