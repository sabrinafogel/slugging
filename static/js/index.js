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
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.add_comment = function(){
//       app.vue.comment_list.push(app.vue.new_comment);
//       app.vue.new_comment = "";
         axios.post(add_messages_url,
         {
           text: app.vue.new_comment
//           alignRight: false// Set alignRight to true for right-aligned messages
         }).then(function(response){
          app.vue.comment_list.push({
              id:response.data.id,
              text: app.vue.new_comment,
          });
          app.enumerate(app.vue.comment_list);
          app.vue.new_comment = ""; // Clear the new comment input field
         });
      };


//working
//         app.vue.comment_list.push({
//         text: app.vue.new_comment,
//         alignRight: false// Set alignRight to true for right-aligned messages
//         });
//         app.vue.new_comment = "";
//    }
//working

    // initialize the map
    app.initMap = function(view){
        // map location: Santa Cruz
        const sc = { lat: 36.974117, lng: -122.030792 };
        
        // center the map on santa cruz
        const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: sc,
        });

        // markers for drivers
        if (view == 1){
            const marker = new google.maps.Marker({
                position: sc,
                map: map,
                label: {
                    text: 'Driver Name',
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

        // markers for riders
        if (view == 2){
            const marker = new google.maps.Marker({
                position: sc,
                map: map,
            });
        }
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

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_comment: app.add_comment,
        viewChange: app.viewChange,
        initMap: app.initMap,
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
        //new
        axios.get(load_messages_url).then(function(response){
            app.vue.comment_list = app.enumerate(response.data.comment_list); //add index to each elem of array
        });
        //new
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
