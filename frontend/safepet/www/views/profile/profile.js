angular.module('safePet')

.controller('profileController', ['$scope','userDogsResource','$auth','$state','userInfo', '$ionicModal', 'usersResource', function($scope,userDogsResource, $auth,$state, userInfo, $ionicModal, usersResource){
	// User information for the view
	$scope.User = {}
	// Handle user information
	userInfo.user.$promise.then(function(user){
		$scope.User.email = user.email;
	    $scope.User.phone = user.phone;
	    $scope.User.address = user.address;
		$scope.User.displayName = user.displayName;
		$scope.User.picture = user.picture;
		$scope.User.id = user._id;
		console.log($scope.User);
	});

	
	$scope.editProfile = function(User){
		usersResource.update({id: $scope.User.id},{data: $scope.User});
		$scope.editModal.hide();
	};

	// Create and load the Modal
    $ionicModal.fromTemplateUrl('edit.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.editModal = modal;
    });

    // Open new task modal
    $scope.edit = function() {
        $scope.editModal.show();
    };

    // Close the new task modal
    $scope.closeEdit = function() {
        $scope.editModal.hide();
    };	
}]);
