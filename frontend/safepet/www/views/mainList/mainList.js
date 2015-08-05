angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', '$resource','$state','$auth', function($scope,$ionicModal,$resource,$state,$auth){

  if(!$auth.isAuthenticated()){
    $state.go("login");
  }
  //Handle dogs information from API
  Dog = $resource("http://safepetapi.labcomp.cl:5000/api/dogs/:id",{id: "@id"});
  $scope.dogs = Dog.query();

  // Create and load the Modal
  $ionicModal.fromTemplateUrl('newDog.html', function(modal) {
    $scope.dogModal = modal;
  }, {
    scope: $scope,
    animation: 'slide-in-up'
  });

  // Called when the form is submitted
  $scope.createDog = function(dog) {
    $scope.dog = {};
    Dog.save(dog);
    $scope.dogModal.hide();
    $scope.dogs.push(dog);
    $scope.dog = {};
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