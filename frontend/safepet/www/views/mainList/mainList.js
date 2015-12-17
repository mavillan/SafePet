angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', 'userDogsResource','dogsResource','$state','$auth','userInfo', 'Camera', function($scope,$ionicModal,userDogsResource,dogsResource,$state,$auth,userInfo,Camera){

    // If the user is not authenticated redirect to the login
    if(!$auth.isAuthenticated()){
        $state.go("login");
    };

    // Refresh user information
    userInfo.refresh();

    // Handle User dogs from the API.
    userInfo.user.$promise.then(function(user){
        $scope.dogs = userDogsResource.query({id: user._id});
    });

    // Find all lost dogs.
    $scope.lostdogs = dogsResource.query();

    // create a new dog when the form is submitted
    $scope.createDog = function(dog) {
        // Add owner id to the dog info
        dog.userId = userInfo.user._id;

        // Save new dog and refreshing dog list in the callback
        dogsResource.save(dog,function(){
            $scope.dogs = userDogsResource.query({id: userInfo.user._id});
        });

        $scope.dogModal.hide();
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

