angular.module('safePet')

.controller('profileController', ['$scope','userDogsResource','$auth','$state','userInfo', function($scope,userDogsResource, $auth,$state, userInfo){
	// User information for the view
	$scope.User = {}
	// Handle user information
	userInfo.user.$promise.then(function(user){
		$scope.User.email = user.email;
	    $scope.User.phone = user.phone;
	    $scope.User.address = user.address;
		$scope.User.displayName = user.displayName;
		$scope.User.id = user._id;
		$scope.dogs = userDogsResource.query({id: user._id});
	});
}]);
