angular.module('safePet')

.controller('editController', ['$scope','$auth','$state','userInfo','usersResource', function($scope,$auth,$state, userInfo, usersResource){
	
	// User information for the view
	$scope.User = {}

	// Handle user information
	userInfo.user.$promise.then(function(user){
		$scope.User.email = user.email;
	    $scope.User.phone = user.phone;
	    $scope.User.address = user.address;
		$scope.User.displayName = user.displayName;
		$scope.User.id = user._id;
	});

	$scope.editProfile = function(User){
		usersResource.update({id: $scope.User.id},{data: $scope.User},function(){
			userInfo.user.$promise.then(function(user){
				$scope.User.email = user.email;
				$scope.User.phone = user.phone;
				$scope.User.address = user.address;
				$scope.User.displayName = user.displayName;
				$scope.User.id = user._id;
			});      
		});		
	};
	
}]);
