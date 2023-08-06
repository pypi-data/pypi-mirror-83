# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2019 Benjamin Marandel - All Rights Reserved.
################################################################################

"""
This module defines the class ESTPPolicyOnAccessScan.
"""

import xml.etree.ElementTree as et
from ...policies import Policy

class ESTPPolicyOnAccessScan(Policy):
    """
    The ESTPPolicyOnAccessScan class can be used to edit the ENS Threat Prevention policy: On-Access Scan.
    """

    def __init__(self, policy_from_estppolicies):
        super(ESTPPolicyOnAccessScan, self).__init__(policy_from_estppolicies)
        if self.get_type() != 'EAM_General_Policies':
            raise ValueError('Wrong ENS Threat Prevention policy. Policy type must be "EAM_General_Policies".')

    def __repr__(self):
        return 'ESTPPolicyOnAccessScan()'
		
    # ------------------------------ On-Access Policy ------------------------------
    # On-Access Scan:
    #   Enable On-Access Scan
    def get_on_access_scan(self):
        """
        Get the On-Access Scan feature state
        """
        return self.get_setting_value('General', 'bOASEnabled')

    def set_on_access_scan(self, mode):
        """
        Set the On-Access Scan feature state
        """
        return self.set_setting_value('General', 'bOASEnabled', mode)

    on_access_scan = property(get_on_access_scan, set_on_access_scan)

    #	Enable On-Access Scan on system startup
    def get_scan_on_startup(self):
        """
        Get the On-Access Scan on system startup state
        """
        return self.get_setting_value('General', 'bStartEnabled')
	
    def set_scan_on_startup(self, mode):
        """
        Set the On-Access Scan on system startup state
        """
        return self.set_setting_value('General', 'bStartEnabled', mode)

    scan_on_startup = property(get_scan_on_startup, set_scan_on_startup)

	#	Allow users to disable On-Access Scan from the McAfee system tray icon
    def get_allow_user_to_disable_oas(self):
        """
        Get state of Allow users to disable On-Access Scan from the McAfee system tray icon
        """
        return self.get_setting_value('General', 'bAllowDisableViaMcTray')

    def set_allow_user_to_disable_oas(self, mode):
        """
        Set state of Allow users to disable On-Access Scan from the McAfee system tray icon
        """
        return self.set_setting_value('General', 'bAllowDisableViaMcTray', mode)

    allow_user_to_disable_oas = property(get_allow_user_to_disable_oas, set_allow_user_to_disable_oas)

    #	Specify maximum number of seconds for each file scan
    def get_max_scan_time_enforced(self):
        """
        Get if maximum scan time is enforced
        """
        return self.get_setting_value('General', 'bEnforceMaxScanTime')
		
    def set_max_scan_time_enforced(self, mode):
        """
        Set enforcement of maximum scan time
        """
        return self.set_setting_value('General', 'bEnforceMaxScanTime', mode)
		
    max_scan_time_enforced = property(get_max_scan_time_enforced, set_max_scan_time_enforced)
	
    def get_max_scan_time(self):
        """
        Get the maximum number of seconds for each file scan
        """
        return int(self.get_setting_value('General', 'dwScannerThreadTimeout'))
		
    def set_max_scan_time(self, int_seconds):
        """
        Set the maximum number of seconds for each file scan
        """
        if int_seconds < 10:
            raise ValueError('Timeout below 10 seconds is not accepted.')
        return self.set_setting_value('General', 'dwScannerThreadTimeout', int_seconds)
		
    max_scan_time = property(get_max_scan_time, set_max_scan_time)
	
    #	Scan boot sectors
    def get_scan_boot_sectors(self):
        """
        Get state of Scan boot sectors
        """
        return self.get_setting_value('General', 'bScanBootSectors')
		
    def set_scan_boot_sectors(self, mode):
        """
        Set state of Scan boot sectors
        """
        return self.set_setting_value('General', 'bScanBootSectors', mode)
		
    scan_boot_sectors = property(get_scan_boot_sectors, set_scan_boot_sectors)
	
    #	Scan processes on service startup and content update
    def get_scan_process_startup(self):
        """
        Get state of Scan processes on service startup and content update
        """
        return self.get_setting_value('General', 'scanProcessesOnEnable')
		
    def set_scan_process_startup(self, mode):
        """
        Set state of Scan processes on service startup and content update
        """
        return self.set_setting_value('General', 'scanProcessesOnEnable', mode)
		
    scan_process_startup = property(get_scan_process_startup, set_scan_process_startup)
	
    #	Scan trusted installers
    def get_scan_trusted_installers(self):
        """
        Get state of Scan trusted installers
        """
        return self.get_setting_value('General', 'scanTrustedInstallers')
	
    def set_scan_trusted_installers(self, mode):
        """
        Set state of Scan trusted installers
        """
        return self.set_setting_value('General', 'scanTrustedInstallers', mode)
		
    scan_trusted_installers = property(get_scan_trusted_installers, set_scan_trusted_installers)
	
    #	Scan when copying between local folders
    def get_scan_copy_between_local_folders(self):
        """
        Get state of Scan when copying between local folders
        """
        return self.get_setting_value('General', 'scanCopyLocalFolders')
		
    def set_scan_copy_between_local_folders(self, mode):
        """
        Set state of Scan when copying between local folders
        """
        return self.set_setting_value('General', 'scanCopyLocalFolders', mode)
		
    scan_copy_between_local_folders = property(get_scan_copy_between_local_folders,
                                               set_scan_copy_between_local_folders)
	
    #	Scan when copying from network folders and removable drives
    def get_scan_copy_from_network(self):
        """
        Get state of Scan when copying from network folders and removable drives
        """
        return self.get_setting_value('General', 'scanCopyNetworkRemovable')
		
    def set_scan_copy_from_network(self, mode):
        """
        Set state of Scan when copying from network folders and removable drives
        """
        return self.set_setting_value('General', 'scanCopyNetworkRemovable', mode)
		
    scan_copy_from_network = property(get_scan_copy_from_network, set_scan_copy_from_network)
	
    #	Detect suspicious email attachments
    def get_scan_email_attachments(self):
        """
        Get state of Detect suspicious email attachments
        """
        return self.get_setting_value('General', 'scanEmailAttachments')
		
    def set_scan_email_attachments(self, mode):
        """
        Set state of Detect suspicious email attachments
        """
        return self.set_setting_value('General', 'scanEmailAttachments', mode)
		
    scan_email_attachments = property(get_scan_email_attachments, set_scan_email_attachments)
       
    #	Disable read/write scan of Shadow Copy volumes for SYSTEM process (improves performance) 
    def get_scan_shadow_copy(self):
        """
        Get state of Read/Write scan of Shadow Copy volumes for SYSTEM process
        """
        mode = self.get_setting_value('General', 'scanShadowCopyDisableStatus')
        return '0' if mode == '1' else '1'
	
    def set_scan_shadow_copy(self, mode):
        """
        Set state of Read/Write scan of Shadow Copy volumes for SYSTEM process
        """
        mode = '0' if mode == '1' else '1'
        return self.set_setting_value('General', 'scanShadowCopyDisableStatus', mode)

    scan_shadow_copy = property(get_scan_shadow_copy, set_scan_shadow_copy)

    # ------------------------------ On-Access Policy ------------------------------
    # McAfee GTI:
    #	Enable McAfee GTI 
    #   0 = OFF         Gti().DISABLED
    #   1 = Very Low    Gti().VERY_LOW
    #   2 = Low         Gti().LOW
    #   3 = Medium      Gti().MEDIUM
    #   4 = High        Gti().HIGH
    #   5 = Very High   Gti().VERY_HIGH
    def get_gti_level(self):
        """
        Get the GTI level (Use Gti class from constants)
        """
        return self.get_setting_value('GTI', 'GTISensitivityLevel')
		
    def set_gti_level(self, level):
        """
        Set the GTI level (Use Gti class from constants)
        """
        if level not in ['0', '1', '2', '3', '4', '5']:
            raise ValueError('GTI sensitivity level must be within ["0", "1", "2", "3", "4", "5"].')
        return self.set_setting_value('GTI', 'GTISensitivityLevel', level)

    gti_level = property(get_gti_level, set_gti_level)

    # ------------------------------ On-Access Policy ------------------------------
    # Antimalware Scan Interface:
    #	Enable AMSI (provides enhanced script scanning)
    def get_scan_amsi(self):
        """
        Get state of Enable AMSI (provides enhanced script scanning)
        """
        return self.get_setting_value('General', 'scanUsingAMSIHooks')
        
    def set_scan_amsi(self, mode):
        """
        Set state of Enable AMSI (provides enhanced script scanning)
        """
        return self.set_setting_value('General', 'scanUsingAMSIHooks', mode)
        
    scan_amsi = property(get_scan_amsi, set_scan_amsi)
    
    #	Enable Observe mode (Events are generated but actions are not enforced)
    def get_scan_amsi_observe_mode(self):
        """
        Get state of Enable AMSI Observe mode (Events are generated but actions are not enforced)
        """
        return self.get_setting_value('General', 'enableAMSIObserveMode')
        
    def set_scan_amsi_observe_mode(self, mode):
        """
        Set state of Enable AMSI Observe mode (Events are generated but actions are not enforced)
        """
        return self.set_setting_value('General', 'enableAMSIObserveMode', mode)
        
    scan_amsi_observe_mode = property(get_scan_amsi_observe_mode, set_scan_amsi_observe_mode)

    # ------------------------------ On-Access Policy ------------------------------
    # Threat Detection User Messaging:
    #	Display the On-Access Scan window to users when a threat is detected
    def get_show_alert(self):
        """
        Get state of Display the On-Access Scan window to users when a threat is detected
        """
        return self.get_setting_value('Alerting', 'bShowAlerts')
        
    def set_show_alert(self, mode):
        """
        Set state of Display the On-Access Scan window to users when a threat is detected
        """
        return self.set_setting_value('Alerting', 'bShowAlerts', mode)
    
    show_alert = property(get_show_alert, set_show_alert)
    
    #	Message: (Default = McAfee Endpoint Security detected a threat.)
    def get_alert_message(self):
        """
        Get Threat Detection message
        """
        return self.get_setting_value('Alerting', 'szDialogMessage')
    
    def set_alert_message(self, str_message="McAfee Endpoint Security detected a threat."):
        """
        Set Threat Detection message (256 caracters maximum)
        """
        if len(str_message) == 0 or len(str_message) > 256:
            raise ValueError('The message cannot be empty or longer than 256 caracters.')
        return self.set_setting_value('Alerting', 'szDialogMessage', str_message)
        
    alert_message = property(get_alert_message, set_alert_message)
