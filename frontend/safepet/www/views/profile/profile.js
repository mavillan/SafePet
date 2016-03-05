angular.module('safePet')

.controller('profileController', ['$scope', 'userInfo', 'usersResource', '$stateParams', function($scope,userInfo,usersResource,$stateParams){
	// User information for the view
	$scope.User = {}
	$scope.userId = userInfo.userId;
	//userInfo.refresh();
	//socketConn.emit('rec', {userId: userInfo.userId});
	// Handle user information
	usersResource.get({id: $stateParams.id}, function(user){
		$scope.User.email = user.email;
	    $scope.User.phone = user.phone;
	    $scope.User.address = user.address;
		$scope.User.displayName = user.displayName;
		$scope.User.picture = user.picture;
		$scope.User.id = user._id;
	});
}]);