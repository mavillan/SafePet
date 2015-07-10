// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('safePet', ['ionic'])

.controller('mainListController', ['$scope', '$ionicModal', function($scope,$ionicModal){
  $scope.dogs = [
    {
      name: "Preta",
      breed: "mestizo",
      color: "negra",
      photo: "https://runningforadream.files.wordpress.com/2012/05/perro_negro_foto.jpg"
    },
    {
      name: "Boby",
      breed: "labrador",
      color: "Castaño",
      photo: "http://labrador.reymascotas.com/imagenes/labradores/labrador-041.jpg"
    },
    {
      name: "Cachupin",
      breed: "mestizo",
      color: "Negro con manchas castañas",
      photo: "http://i.ytimg.com/vi/0EcP8Rjo4UQ/hqdefault.jpg"
    },
    {
      name: "Laika",
      breed: "mestizo",
      color: "blanco con manchas negras",
      photo: "http://3.bp.blogspot.com/-k3eVsZW9sDs/VF9-wqtLAYI/AAAAAAAAJ-E/o15l8TfFm0U/s1600/laika.jpg"
    }

  ];

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
