// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        comment_list: [],
        new_comment: "",
        view: 0,

        markerData: [],
        otherUserID: 0,
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.erase_search = function(){
        app.vue.query = ""
        axios.get(get_users_url).then(function(response) {
            app.vue.users = app.enumerate(response.data.all_users);
        });
    };

    app.search = function(){
        if (app.vue.query.length > 0){
            axios.get(search_url, {params: {q: app.vue.query}}).then(function(response) {
                app.vue.users = app.enumerate(response.data.all_users);
                // app.vue.users = []
            });
        }else{
            axios.get(get_users_url).then(function(response) {
                app.vue.users = app.enumerate(response.data.all_users);
            });
        }
    };

    // initialize the map
    app.initMap = function(view){
        // map location: Santa Cruz
        const sc = { lat: 36.974117, lng: -122.030792 };
        
        // center the map on santa cruz
        const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: sc,
        });

        // new google.maps.Marker({
        //     position: { lat: 36.974117, lng: -122.030792 },
        //     map,
        //     title: "Hello World!",
        // });

        // get the database lat and long for markers
        axios.get(driverURL)
            .then(function (response){
                app.vue.markerData = response.data.markerList;
                
                // for bug testing
                console.log(response.data.markerList);
                console.log(app.vue.markerData);

                // markers for drivers
                if (view == 1){
                    for (let i = 0; i < app.vue.markerData.length; i++) {
                        let user = app.vue.markerData[i];
                        if (user.category == "driver") {
                            const marker = new google.maps.Marker({
                                position: {lat: user.location[1], lng: user.location[2]},
                                map: map,
                                label: {
                                    text: user.firstName + " " + user.lastName,
                                    color: 'red',
                                    fontsize: '24px'
                                },
                                icon: {
                                    url: 'https://th.bing.com/th/id/R.45627b4df6c629e3a880121fe0143b17?rik=L7K%2bYZCvUNxlug&riu=http%3a%2f%2fwww.clipartbest.com%2fcliparts%2fyio%2fM5B%2fyioM5BxBT.png&ehk=0MPKSrO21UJbumaqXsH5ULRE9erzktvhZ5DUxUELR4c%3d&risl=&pid=ImgRaw&r=0',
                                    scaledSize: new google.maps.Size(50, 50),
                                    labelOrigin: new google.maps.Point(25, -10)
                                }
                            });
                        }
                    }
                }

                // markers for riders
                if (view == 2){
                    for (let i = 0; i < markerList.length; i++) {
                        let user = markerList[i];
                        if (user.category == "rider") {
                            const marker = new google.maps.Marker({
                                position: {lat: user.location[1], lng: user.location[2]},
                                map: map,
                                label: {
                                    text: user.firstName + " " + user.lastName,
                                    color: 'red',
                                    fontsize: '24px'
                                },
                                icon: {
                                    url: 'https://th.bing.com/th/id/OIP.AtdqxcU3grBhlv6OgXH5hwHaHa?w=219&h=219&c=7&r=0&o=5&dpr=2&pid=1.7',
                                    scaledSize: new google.maps.Size(50, 50),
                                    labelOrigin: new google.maps.Point(25, -10)
                                }
                            });
                        }
                    }
                }
            });
    };

    // change the view from list to map or map to list
    app.viewChange = function(view){
        app.vue.view = view
        if (app.vue.view > 0){
            app.vue.$nextTick(() => {
                app.initMap(view);
            });
        };
    };

    

    // set user id that you are messaging
    app.getUser = function (otherUserID) {
        app.vue.otherUserID = otherUserID
        console.log(app.vue.otherUserID);

        // send user id you are messaging
        axios.post(getUserURL, { id: app.vue.otherUserID })
        .then(function (result) {
 
        });
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        viewChange: app.viewChange,
        initMap: app.initMap,
        getUser: app.getUser,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
