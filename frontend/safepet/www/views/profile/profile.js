angular.module('safePet')

.controller('profileController', ['$scope','userInfo', 'usersResource', 'noseImgs', 'socketConn', function($scope,userInfo,usersResource,noseImgs, socketConn){
	// User information for the view
	$scope.User = {}
	userInfo.refresh();
	socketConn.emit('rec', {userId: userInfo.userId});
	// Handle user information
	userInfo.user.$promise.then(function(user){
		$scope.User.email = user.email;
	    $scope.User.phone = user.phone;
	    $scope.User.address = user.address;
		$scope.User.displayName = user.displayName;
		$scope.User.picture = user.picture;
		$scope.User.id = user._id;
	});
}]);
