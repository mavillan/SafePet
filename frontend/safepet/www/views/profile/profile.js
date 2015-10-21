angular.module('safePet')

.controller('profileController', ['$scope','userDogsResource','$auth','$state','userInfo', function($scope,userDogsResource, $auth,$state, userInfo){
	userInfo.user.$promise.then(function(user){
	    $scope.datos = {address: user.address, phoneNumber: user.phone};
		$scope.nickname = user.displayName;
		$scope.dogs = userDogsResource.query({id: user._id});
	});
}]);
