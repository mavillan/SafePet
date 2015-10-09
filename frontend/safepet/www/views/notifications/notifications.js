angular.module('safePet')
.controller('notificationsController', ['$scope','$ionicLoading','$auth', '$state',function($scope,$ionicLoading,$auth,$state){
	if(!$auth.isAuthenticated()){
        $state.go("login");
    }

	$scope.not = function(){
		$ionicLoading.show({
      		template: 'Loading...'
    	});
	}
}])