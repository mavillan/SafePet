angular.module('safePet')


.controller('menuController', ['$scope','$auth','$state','userInfo', function($scope,$auth,$state,userInfo){

	userInfo.$promise.then(function(user){
		$scope.menuTitle = user.displayName;
	});
	
	$scope.logout = function(){
		$auth.logout()
		.then(function() {
            $state.go("login");
        });
	};
	
}]);