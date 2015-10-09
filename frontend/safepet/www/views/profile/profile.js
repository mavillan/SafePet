angular.module('safePet')

.controller('profileController', ['$scope','userDogsResource','$auth','$state','userInfo', function($scope,userDogsResource, $auth,$state, userInfo){
        $scope.datos = {address: 'Valparaiso', phoneNumber: '+56912345678'};
	userInfo.$promise.then(function(user){
		$scope.nickname = user.displayName;
		$scope.dogs = userDogsResource.query({id: user._id});
		$scope.size = $scope.dogs.length;
	});
}]);
