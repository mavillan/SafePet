angular.module('safePet', ['ionic','ngResource'])

.controller('mainListController', ['$scope', '$ionicModal', '$resource', function($scope,$ionicModal,$resource){
  
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
    $scope.dogs.push({
      name: dog.name,
      breed: dog.breed,
      color: dog.color,
    });
    $scope.dogModal.hide();
    dog.name = "";
    dog.breed = "";
    dog.color = "";
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
