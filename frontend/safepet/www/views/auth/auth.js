angular.module('safePet')

.controller('authController', ['$scope','$auth','$state','$ionicModal', '$ionicPopup', function($scope,$auth,$state,$ionicModal,$ionicPopup){
    $scope.signup = function(user) {
        $auth.signup({
        	displayName: user.displayName,
            email: user.email,
            password: user.password
        })
        .then(function() {
        	$scope.userModal.hide();
            $state.go("app.mainList");
        })
        .catch(function(response) {
        	$ionicPopup.alert({
        	  title: 'Error',
        	  content: response.data ? response.data || response.data.message : response
        	});
        });
    }
    $scope.login = function(user){
        $auth.login({
        	displayName: user.displayName,
            email: user.email,
            password: user.password
        })
        .then(function(){
            $state.go("app.mainList")
        })
        .catch(function(response){
        	$ionicPopup.alert({
        	  title: 'Error',
        	  content: response.data ? response.data || response.data.message : response
        	})
        });
    }
	// Create and load the Modal
	$ionicModal.fromTemplateUrl('newUser.html', function(modal) {
		$scope.userModal = modal;
	}, {
		scope: $scope,
		animation: 'slide-in-up'
	});

	// Open our new task modal
	$scope.newUser = function() {
	  	$scope.userModal.show();
	};

  	// Close the new task modal
	$scope.closeNewUser = function() {
		$scope.userModal.hide();
	};
}]);