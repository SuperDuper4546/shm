#!/usr/bin/perl

use strict;
use warnings;
use v5.14;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

use Core::System::ServiceManager qw(get_service);
use Core::Utils qw(parse_args trim);
use SHM qw(:all);

my $cgi = CGI->new;
my $user = SHM->new(skip_check_auth => 1);
my %in = parse_args();

my $config  = get_service('config');

if ($in{register}) {
    unless ($in{login} && $in{password}) {
        print_json({ status => 400, msg => 'Login and password are required' });
        exit 0;
    }
    
    if ($user->exists(login => trim($in{login}))) {
        print_json({ status => 409, msg => 'User already exists' });
        exit 0;
    }
    
    my $new_user = SHM->new;
    $new_user->set(login => trim($in{login}), password => trim($in{password}));
    $new_user->commit;
    
    print_json({ status => 201, msg => 'User registered successfully' });
    exit 0;
}
