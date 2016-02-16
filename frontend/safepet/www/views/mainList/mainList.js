angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', 'userDogsResource','dogsResource','$state','$auth','userInfo', 'Camera', '$http', '$interval', 'lostDogs', 'socketConn', '$cordovaFileTransfer',  '$cordovaImagePicker', function($scope,$ionicModal,userDogsResource,dogsResource,$state,$auth,userInfo,Camera, $http, $interval, lostDogs, socketConn, $cordovaFileTransfer,  $cordovaImagePicker){

    // If the user is not authenticated redirect to the login
    if(!$auth.isAuthenticated()){
        $state.go("login");
    };
    //Results
    $scope.dogsScanList = [];
   
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
    $ionicModal.fromTemplateUrl('newDog2.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.dogModal2 = modal;
    });

    // Open new task modal
    $scope.newDog = function() {
        $scope.dogModal2.hide();
        $state.go("app.newdog");
    };

    $scope.newDog2 = function() {
        $scope.dogModal2.show();
    };

    $scope.closeNewDog2 = function() {
        $scope.dogModal2.hide();
    };
    // Create and load the Modal Crop
    $ionicModal.fromTemplateUrl('imgCrop.html', function(modal) {
        $scope.cropModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    $scope.opentest = function(){
        console.log($scope.dogsScanList.length);
        $scope.dogsScan.show();   
    }

    //Dog Scan List modal
    $ionicModal.fromTemplateUrl('dogsScan.html', function(modal) {
        $scope.dogsScan = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });
    $scope.openDogsScan = function() {
        $scope.dogsScan.show();
    }
    $scope.closeDogsScan = function() {
        $scope.dogsScan.hide();
        $scope.dogsScanList = [];
    };


    //Upload image from galery
    //$scope.collection = [];
    
    $scope.getImageGalery = function(){
        var options = {
            maximumImagesCount: 1,
            width: 500,
            height: 500,
            quality: 75
        };

        $cordovaImagePicker.getPictures(options).then(function (results) {
            for (var i = 0; i < results.length; i++) {
                console.log('Image URI: ' + results[i]);
                //$scope.collection.push(results[i]);
                $scope.lastPhoto = results[i];
            }
        }, function(error) {
            console.err(err);
        });
    };

    $scope.upload = function (img) {
        //target path may be local or url
        $scope.cropModal.hide();
        //var filename = targetPath.split("/").pop();
        var targetPath = $scope.picFile;
        var options = {
            fileKey: "file",
            fileName: "scan.jpg",
            chunkedMode: false,
            mimeType: "image/jpg"
        };
        $cordovaFileTransfer.upload("http://safepetapi.labcomp.cl:5000/scannose", targetPath, options).then(function(result) {
            //alert("¡Imagen Valida!");
            result.response.forEach(function(item){
                dogsResource.get({id: item}, function(dog){
                    $scope.dogsScanList.push(dog)
                });
            });
        });
        $scope.openDogsScan();
    };

    //Get a photo
    $scope.getPhoto = function() {
        Camera.getPicture({
            quality: 100,
            targetWidth: 500,
            targetHeight: 500,
            saveToPhotoAlbum: false
        }).then(function(imageURI){
            //Scan Nose
            $scope.picFile = imageURI;
            $scope.cropModal.show();
        }, function(err) {
            console.err(err);
        });
    
        navigator.camera.getPicture(function(imageURI) {
            console.log(imageURI);
        }, function(err) {
        }, { 
            quality: 100,
            destinationType: Camera.DestinationType.DATA_URL
        });
    };
}]);

