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
        view: 'list',
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
    app.initMap = function(){
        // map location: Santa Cruz
        const sc = { lat: 36.974117, lng: -122.030792 };
        
        // center the map on santa cruz
        const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: sc,
        });
    };

    // change the view from list to map or map to list
    app.viewChange = function(view){
        app.vue.view = view
        if (app.vue.view == 'map'){
            app.vue.$nextTick(() => {
                app.initMap();
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
