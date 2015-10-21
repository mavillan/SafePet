angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', 'userDogsResource','dogsResource','$state','$auth','userInfo', function($scope,$ionicModal,userDogsResource,dogsResource,$state,$auth,userInfo){

    // If the user is not authenticated redirect to the login
    if(!$auth.isAuthenticated()){
        $state.go("login");
    }

    // Refresh user information
        userInfo.refresh();

    // Handle User dogs from the API.
    userInfo.user.$promise.then(function(user){
        $scope.dogs = userDogsResource.query({id: user._id});
    });

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
    $ionicModal.fromTemplateUrl('newDog.html', function(modal) {
        $scope.dogModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    // Open new task modal
    $scope.newDog = function() {
        $scope.dogModal.show();
    };

    // Close the new task modal
    $scope.closeNewDog = function() {
        $scope.dogModal.hide();
    };

}]);

