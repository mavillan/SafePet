angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', 'dogsResource','$state','$auth','userInfo', function($scope,$ionicModal,dogsResource,$state,$auth,userInfo){


  if(!$auth.isAuthenticated()){
    $state.go("login");
  }


  //Handle dogs information from API
  $scope.dogs = dogsResource.query();

  // Create and load the Modal
  $ionicModal.fromTemplateUrl('newDog.html', function(modal) {
    $scope.dogModal = modal;
  }, {
    scope: $scope,
    animation: 'slide-in-up'
  });

  // create a new dog when the form is submitted
  $scope.createDog = function(dog) {
    // Add owner id to the dog info
    dog.userId = userInfo._id;

    //Save new dog
    dogsResource.save(dog);
    
    // Refresh dogs list
    $scope.$apply(function(){
      $scope.dogs = dogsResource.query();
    });
    $scope.dogModal.hide();
  };

  // Open our new task modal
  $scope.newDog = function() {
    $scope.dogModal.show();
  };

  // Close the new task modal
  $scope.closeNewDog = function() {
    $scope.dogModal.hide();
  };
}]);