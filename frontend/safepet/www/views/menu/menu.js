angular.module('safePet')


.controller('menuController', ['$scope','$auth','$state','userInfo','$ionicHistory','$timeout', function($scope,$auth,$state,userInfo,$ionicHistory,$timeout){

	// Refresh user information
	userInfo.refresh();

	if($auth.isAuthenticated()){
	// Handle user information from the API
	userInfo.user.$promise.then(function(user){
		userInfo.refresh();
		$scope.menuTitle = user.displayName;
	});
	
	}
	$scope.logout = function(){
		$auth.logout()
		.then(function() {
			userInfo.clear();
            $state.go("login");
    		$timeout(function () {
        		$ionicHistory.clearCache();
        		$ionicHistory.clearHistory();
    		}, 1500)
        });
	};
	
}]);