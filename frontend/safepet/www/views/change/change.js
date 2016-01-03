angular.module('safePet')


.controller('changeController', ['$scope','$stateParams', '$ionicPopup', 'changeOwner', 'usersResource', function($scope,$stateParams, $ionicPopup, changeOwner, usersResource){
	$scope.change = function(user) {
		var confirmAlert = $ionicPopup.confirm({
			title: "Cambiar dueño",
			template: "¿Está seguro que quiere cambiar de dueño a su mascota?"
		}).then(function(res){
			if(res){
				console.log("Realizar cambio");
			}
		});
		console.log($stateParams.dogId);
	};
}]);
