angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', 'userDogsResource','dogsResource','$state','$auth','userInfo', 'Camera', '$http', '$interval', 'lostDogs', '$cordovaImagePicker', '$ionicPlatform', 'socketConn', function($scope,$ionicModal,userDogsResource,dogsResource,$state,$auth,userInfo,Camera, $http, $interval, lostDogs, $cordovaImagePicker, $ionicPlatform, socketConn){

    // If the user is not authenticated redirect to the login
    if(!$auth.isAuthenticated()){
        $state.go("login");
    };

    // Refresh user information
    userInfo.refresh();
    socketConn.on('changeAccepted', function(){
        userInfo.refresh();
    });
    // Handle User dogs from the API with
    // Event listener: update dog list
    $scope.$on('user:refresh', function(event, data){        
        $scope.dogs = data.dogs;
    });

    // create a new dog when the form is submitted
    $scope.createDog = function(dog) {
        // Add owner id to the dog info
        dog.userId = userInfo.user._id;

        // Save new dog and refreshing dog list in the callback
        dogsResource.save(dog,function(){
            $scope.dogs = userDogsResource.query({id: userInfo.user._id});
            userInfo.refresh();
        });

        $scope.dogModal.hide();
    };

    // Find all lost dogs.
    $scope.lostdogs = lostDogs.query();
    // Update list on state change
    $scope.$on('dog:lost', function(event, data){
        $scope.lostdogs = lostDogs.query();
    });
    
    
    //Refresh lost dogs on pull
    $scope.doRefresh = function() {
        $http.get('#/app/mainlist')
        .success(function() {
            $scope.lostdogs = lostDogs.query();
        }).finally(function() {
            // Stop the ion-refresher from spinning
            $scope.$broadcast('scroll.refreshComplete');
        });
    };

    // Create and load the Modal
    $ionicModal.fromTemplateUrl('newDog.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.dogModal = modal;
    });

    // Open new task modal
    $scope.newDog = function() {
        $scope.dogModal.show();
    };

    // Close the new task modal
    $scope.closeNewDog = function() {
        $scope.dogModal.hide();
    };
    // Create and load the Modal Crop
    $ionicModal.fromTemplateUrl('imgCrop.html', function(modal) {
        $scope.cropModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    //ImagePicker

    /*$scope.collection = {
        selectedImage : ''
    };*/

    /*$scope.convertToDataURLviaCanvas = function(url, callback, outputFormat){
        var img = new Image();
        img.crossOrigin = 'Anonymous';
        img.onload = function(){
            var canvas = document.createElement('CANVAS');
            var ctx = canvas.getContext('2d');
            var dataURL;
            canvas.height = this.height;
            canvas.width = this.width;
            ctx.drawImage(this, 0, 0);
            dataURL = canvas.toDataURL(outputFormat);
            callback(dataURL);
            canvas = null; 
        };
        img.src = url;
    };*/

    $scope.collection = [];
    //$scope.b64 = [];

    $scope.getImageGalery = function(){
        var options = {
            maximumImagesCount: 5,
            width: 500,
            height: 500,
            quality: 75
        };

        $cordovaImagePicker.getPictures(options).then(function (results) {
            for (var i = 0; i < results.length; i++) {
                console.log('Image URI: ' + results[i]);
                $scope.collection.push(results[i]);
                /*window.plugins.Base64.encodeFile(results[i], function(base64){  // Encode URI to Base64 needed for contacts plugin
                    results[i] = base64;
                    $scope.collection.push(results[i]);
                });
                /*convertToDataURLviaCanvas(results[i], function(base64Img, 'image/jpeg'){
                // Base64DataURL
                });
                /*window.plugins.Base64.encodeFile($scope.collection.selectedImage, function(base64){  // Encode URI to Base64 needed for contacts plugin
                    $scope.collection.selectedImage = base64;
                });*/
            }
        }, function(error) {
            // error getting photos
            console.err(err);
        });
    };

    $scope.fileUpload = function (upImage, par) {
        if (par){
            upIm = 
            upImage = window.atob(upImage);
            $scope.cropModal.hide();
        };
        console.log(upImage);
        // Destination URL 
        var url = "http://localhost:5000/";
      
        //File for Upload
        var targetPath = upImage;//cordova.file.externalRootDirectory + "logo_radni.png";
      
        // File name only
        //var filename = targetPath.split("/").pop();
        var filename = userInfo.user._id;
      
        var options = {
            fileKey: "file",
            fileName: filename,
            chunkedMode: false,
            mimeType: "image/jpg",
            params : {'directory':'upload', 'fileName':filename}
        };
           
        $cordovaFileTransfer.upload(url, targetPath, options).then(function (result) {
            console.log("SUCCESS: " + JSON.stringify(result.response));
        }, function (err) {
            console.log("ERROR: " + JSON.stringify(err));
        }, function (progress) {
          // PROGRESS HANDLING GOES HERE
        });
    };

    // Open new task modal
    $scope.crop = function() {
        $scope.myImage = '';
        $scope.myCroppedImage = '';
        $scope.getPhoto(false);
    };

    // Close the new task modal
    $scope.closeCrop = function() {
        $scope.cropModal.hide();
    };

    $scope.getPhoto = function(opt) {
        console.log('Getting camera');
        Camera.getPicture({
            quality: 75,
            targetWidth: 500,
            targetHeight: 500,
            saveToPhotoAlbum: false
        }).then(function(imageURI){//imageURI) {
            if (opt) {
                $scope.lastPhoto = imageURI;//imageURI;
            } else { 
                $scope.myImage = imageURI;
                $scope.cropModal.show();
            };
        }, function(err) {
            console.err(err);
        });
    
        navigator.camera.getPicture(function(imageURI) {
            console.log(imageURI);
        }, function(err) {
        }, { 
            quality: 75,
            destinationType: Camera.DestinationType.DATA_URL//FILE_URI
        });
    };
}]);

