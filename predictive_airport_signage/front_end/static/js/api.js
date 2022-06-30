function getUrlParameters(){
    let url = window.location.search;
    let urlParams = new URLSearchParams(url);
    return urlParams;
}

function getRequest(url){
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function getArrivals(){
    let arrivals = JSON.parse(getRequest("/api/arrivals"));
    return arrivals;
}

function getDepartures(){
    let departures = JSON.parse(getRequest("/api/departures"));
    return departures;
}
