angular.module('safePet')
.controller('dogDetailsController', ['$scope', '$resource','$stateParams','$state', function($scope,$resource,$stateParams,$state){
	$scope.id = $stateParams.dogId;
	Dog = $resource("http://safepetapi.labcomp.cl:5000/api/dogs/:id",{id: "@id"});
	$scope.dog = Dog.get({id: $stateParams.dogId});
	$scope.deleteDog = function () {
		Dog.delete({id: $stateParams.dogId});
		$state.go('app.mainList');
	};
}]);