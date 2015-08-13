angular.module('safePet')


.controller('menuController', ['$scope','$auth','$state','userInfo', function($scope,$auth,$state,userInfo){

	$scope.menuTitle = userInfo.displayName;
	
	$scope.logout = function(){
		$auth.logout()
		.then(function() {
            $state.go("login");
        });
	};
	
}]);