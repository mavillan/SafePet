angular.module('safePet')

.controller('editController', ['$scope','$auth','$state','userInfo', function($scope,$auth,$state, userInfo){
	$scope.dato = {};
	
	$scope.submit = function() {

	console.log("hola2");
		$scope.datos.push($scope.dato);
		$state.go('app/profile');
    	};
}]);
