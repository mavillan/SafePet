angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', 'userDogsResource','dogsResource','$state','$auth','userInfo', 'Camera', '$http', '$interval', 'lostDogs', 'socketConn', function($scope,$ionicModal,userDogsResource,dogsResource,$state,$auth,userInfo,Camera, $http, $interval, lostDogs, socketConn){

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
        $scope.dogModal.show();
    };

    $scope.newDog2 = function() {
        $scope.dogModal2.show();
    };

    // Close the new task modal
    $scope.closeNewDog = function() {
        $scope.dogModal.hide();
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

    // Open new task modal
    $scope.crop = function() {
        $scope.myImage = '';
        $scope.myCroppedImage = '';
        $scope.getPhoto();
        //$scope.cropModal.show();
    };

    // Close the new task modal
    $scope.closeCrop = function() {
        $scope.cropModal.hide();
    };


    $scope.getPhoto = function() {
        console.log('Getting camera');
        Camera.getPicture({
        quality: 75,
        targetWidth: 500,
        targetHeight: 500,
        saveToPhotoAlbum: false
        }).then(function(imageURI) {
            //console.log(imageURI);
            $scope.lastPhoto = imageURI;
           /* $scope.showAlert = function() {
        var alertPopup = $ionicPopup.alert({
                title: 'Acerca de SafePet',
                template: '{{lastPhoto}}' 
        });
    };
            $scope.showAlert();*/
            $scope.myImage = imageURI;
            $scope.cropModal.show();

        }, function(err) {
        console.err(err);
    });
    
        navigator.camera.getPicture(function(imageURI) {
            console.log(imageURI);
        }, function(err) {
        }, { 
            quality: 50,
            destinationType: Camera.DestinationType.DATA_URL
        });
    };
}]);

