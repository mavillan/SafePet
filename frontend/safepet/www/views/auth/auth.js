angular.module('safePet')

.controller('authController', ['$scope','$auth','$state','$ionicModal', function($scope,$auth,$state,$ionicModal){
    var vm = this;
    this.signup = function() {
        $auth.signup({
        	displayName: vm.displayName,
            email: vm.email,
            password: vm.password
        })
        .then(function() {
            $state.go("app.mainList");
        })
        .catch(function(response) {
        });
    }
    this.login = function(){
        $auth.login({
        	displayName: vm.displayName,
            email: vm.email,
            password: vm.password
        })
        .then(function(){

            $state.go("app.mainList")
        })
        .catch(function(response){

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
}])

.controller('LogoutController', ['$scope','$auth','$state', function($scope,$auth,$state){
    $auth.logout()
        .then(function() {

            $state.go("login")
        });
}]);