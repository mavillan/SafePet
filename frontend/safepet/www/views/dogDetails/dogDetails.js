angular.module('safePet')
.controller('dogDetailsController', ['$scope', 'dogsResource','$stateParams','$state', function($scope,dogsResource,$stateParams,$state){

	$scope.dog = dogsResource.get({id: $stateParams.dogId});

	$scope.deleteDog = function () {
		dogsResource.delete({id: $stateParams.dogId});
		
		$state.go('app.mainList');
	};
}]);