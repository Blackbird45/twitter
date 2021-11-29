let map;

function initMap() {

    const myLatlng = { lat: -25.363, lng: 131.044 };

    map = new google.maps.Map(document.getElementById("map"), {
        center: myLatlng,
        zoom: 8,
    });
    const marker = new google.maps.Marker({
        position: myLatlng,
        map,
        title: "Click to zoom",
    });
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
        content: "Click the map to get Lat/Lng!",
        position: myLatlng,
    });

    map.addListener("center_changed", () => {
        // 3 seconds after the center of the map has changed, pan back to the
        // marker.
        window.setTimeout(() => {
            map.panTo(marker.getPosition());
        }, 3000);
    });
    marker.addListener("click", () => {
        map.setZoom(8);
        map.setCenter(marker.getPosition());
    });
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
            position: mapsMouseEvent.latLng,
        });
        infoWindow.setContent(
            JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
        );
        infoWindow.open(map);

        map.setCenter(mapsMouseEvent.latLng);
    });
}