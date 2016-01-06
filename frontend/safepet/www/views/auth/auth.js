angular.module('safePet')

.controller('authController', ['$scope','$auth','$state','$ionicModal', '$ionicPopup', 'userInfo', 'socketConn', '$rootScope', function($scope,$auth,$state,$ionicModal,$ionicPopup, userInfo, socketConn, $rootScope){
    $scope.signup = function(user) {
        $auth.signup({
        	displayName: user.displayName,
            email: user.email,
            password: user.password,
            address: user.address,
            phone: user.phone
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
    };
    $scope.login = function(user){
        $auth.login({
        	displayName: user.displayName,
            email: user.email,
            password: user.password
        })
        .then(function(){
            userInfo.refresh();
            socketConn.emit("login", {userId: userInfo.userId});
            $state.go("app.mainList")
        })
        .catch(function(response){
        	$ionicPopup.alert({
        	  title: 'Error',
        	  content: 'Usuario o contraseña incorrectos'//response.data ? response.data || response.data.message : response
        	})
        });
    };

    //Facebook Login
    $scope.authenticate = function(provider) {
      $auth.authenticate(provider)
        .then(function() {
            userInfo.refresh();
            socketConn.emit("login", {userId: userInfo.userId});
            $state.go("app.mainList")
        })
        .catch(function(response) {
          $ionicPopup.alert({
            title: 'Error',
            content: response.data ? response.data || response.data.message : response
          })

        });
    };

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