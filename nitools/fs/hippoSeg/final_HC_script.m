function usman_HC_test_script_fp

%% RUN IN DIRECTORY
%array=dirdir(pwd,1)
%array=fp_limit(array,'FS')
%subdir='27-04-2012_usman_HF/'
%%%%%written by Usman Khan (uak2105@columbia.edu) and Frank Provenzano (fap2005@columbia.edu) , Scott Small Laboratory, Taub Institute, Columbia University%%%%
% decide whether it's a function or a predefined cell {Nx1}
% subdir requires end slash i.e. 'april_25_proc/
if nargin<2
    if nargin<1
        array={};
        array{1,1}=pwd;
    end
    subdir='';
end
%%%%%%%%%%LEFT SIDE%%%%%%%%%%%%
 for ii1=1:size(array,1)
    case_array_l={'posterior_left_CA1.nii.gz' , 'posterior_left_CA2-3.nii.gz' , 'posterior_left_CA4-DG.nii.gz' , 'posterior_left_fimbria.nii.gz' , 'posterior_left_hippocampal_fissure.nii.gz' , 'posterior_Left-Hippocampus.nii.gz' , 'posterior_left_presubiculum.nii.gz' , 'posterior_left_subiculum.nii.gz'};
    current_dir=dirfile(pwd);
    temp=fp_limit(current_dir,'left_CA1');
    case_array_l{1,1}=temp{1};
    temp=fp_limit(current_dir,'left_CA2-3');
    case_array_l{1,2}=temp{1};
    temp=fp_limit(current_dir,'left_CA4-DG');
    case_array_l{1,3}=temp{1};
    temp=fp_limit(current_dir,'left_fimbria');
    case_array_l{1,4}=temp{1};
    temp=fp_limit(current_dir,'left_hippocampal_fissure');
    case_array_l{1,5}=temp{1};
    temp=fp_limit(current_dir,'Left-Hippocampus');
    case_array_l{1,6}=temp{1};
    temp=fp_limit(current_dir,'left_presubiculum');
    case_array_l{1,7}=temp{1};
    temp=fp_limit(current_dir,'left_subiculum');
    case_array_l{1,8}=temp{1};
   
    for ij1=1:size(case_array_l,2)
        case_array_l{1,ij1}=[array{ii1,1} filesep subdir case_array_l{1,ij1}];
    end
    imgarrayl=case_array_l;
    NumLabel_l=length(imgarrayl);
    volmaskl=MRIread(imgarrayl{1,1});
    [vsz1l vsz2l vsz3l] = size(volmaskl.vol);
    volmaskzerol.vol=zeros(vsz1l, vsz2l, vsz3l);
    volmaskl.vol=volmaskzerol.vol;
    volmaxl.vol=volmaskzerol.vol;
    
    for i = 1:NumLabel_l
        vol=MRIread(imgarrayl{1,i});
        eval(['vol' num2str(i) '=vol']);
        if i==1
            sumvol=volmaxl;
        end
        clear vol;
        size(volmaskl.vol);
        size(volmaxl.vol);
        curvol=eval(['vol' num2str(i) '.vol']);
        volmaskl.vol(find(curvol>= volmaxl.vol))=i;
        volmaxl.vol(find(curvol >= volmaxl.vol))=curvol(find(curvol>=volmaxl.vol));
        sumvol.vol=sumvol.vol+curvol;
        if i==NumLabel_l
            sumvol1=sumvol.vol;
            sumvol1(find(sumvol1>0))=1;
            volmaskl.vol=volmaskl.vol.*sumvol1;
        end
    end
    %[array{ii1,1} filesep subdir 'HC_subfield_combined_L.nii.gz']
    %pause
    MRIwrite(volmaskl,[array{ii1,1} filesep subdir 'HC_subfield_combined_L.nii.gz'])
 end
clear curvol
clear volmaskl
clear volmaxl
%%%%%%%%%%%RIGHT SIDE%%%%%%%%%%%%%%%%
 for ii2=1:size(array,1)
    %%%%%%%%%%load files for left and right separately since they have unequal ijk/xyz dimensions%%%%
    case_array_r={'posterior_right_CA1.nii.gz' , 'posterior_right_CA2-3.nii.gz' , 'posterior_right_CA4-DG.nii.gz' , 'posterior_right_fimbria.nii.gz' , 'posterior_right_hippocampal_fissure.nii.gz' , 'posterior_Right-Hippocampus.nii.gz' , 'posterior_right_presubiculum.nii.gz' , 'posterior_right_subiculum.nii.gz'};
    temp=fp_limit(current_dir,'right_CA1');
    case_array_r{1,1}=temp{1};
    temp=fp_limit(current_dir,'right_CA2-3');
    case_array_r{1,2}=temp{1};
    temp=fp_limit(current_dir,'right_CA4-DG');
    case_array_r{1,3}=temp{1};
    temp=fp_limit(current_dir,'right_fimbria');
    case_array_r{1,4}=temp{1};
    temp=fp_limit(current_dir,'right_hippocampal_fissure');
    case_array_r{1,5}=temp{1};
    temp=fp_limit(current_dir,'Right-Hippocampus');
    case_array_r{1,6}=temp{1};
    temp=fp_limit(current_dir,'right_presubiculum');
    case_array_r{1,7}=temp{1};
    temp=fp_limit(current_dir,'right_subiculum');
    case_array_r{1,8}=temp{1};
   
    for ij2=1:size(case_array_r,2)
        case_array_r{1,ij2}=[array{ii2,1} filesep subdir case_array_r{1,ij2}];
    end
    imgarrayr=case_array_r
    NumLabel_r=length(imgarrayr)
    
    volmaskr=MRIread(imgarrayr{1,1});
    [vsz1r vsz2r vsz3r] = size(volmaskr.vol);
    volmaskzeror.vol=zeros(vsz1r, vsz2r, vsz3r);
    volmaskr.vol=volmaskzeror.vol;
    volmaxr.vol=volmaskzeror.vol;
    
    for i = 1:NumLabel_r
        vol=MRIread(imgarrayr{1,i});
        eval(['vol' num2str(i) '=vol']);
        if i==1
            sumvol=volmaxr;
        end
        clear vol;
        size(volmaskr.vol);
        size(volmaxr.vol);
        curvol=eval(['vol' num2str(i) '.vol']);
        volmaskr.vol(find(curvol>= volmaxr.vol))=i;
        volmaxr.vol(find(curvol >= volmaxr.vol))=curvol(find(curvol>=volmaxr.vol));
        sumvol.vol=sumvol.vol+curvol;
        if i==NumLabel_l
            sumvol1=sumvol.vol;
            sumvol1(find(sumvol1>0))=1;
            volmaskr.vol=volmaskr.vol.*sumvol1;
        end
    end
    
    MRIwrite(volmaskr,[array{ii2,1} filesep subdir 'HC_subfield_combined_R.nii.gz'])
 end
 
 function df = dirfile(dirstr,~)
% dirfile(dirstr,fullpath) - returns a cell array of filenames in
% the input directory dirstr.  Add a second argument to flag for return
% of full file paths instead of filenames.
if nargin == 0,
    dirstr = pwd;
end
if isempty(strmatch('/',dirstr)),
    dirstr = [pwd '/' dirstr];
end
if isempty(strmatch('/',dirstr(end))),
    if exist([dirstr '/'],'dir')
        basedir = [dirstr '/'];
    else
        basedir = [fileparts(dirstr) '/'];
    end
else
    basedir = dirstr;
end
dfall = dir(dirstr);
names = {dfall.name}';
df = names(~[dfall.isdir]');
if nargin > 1,
    for i=1:length(df)
        df{i} = [basedir df{i}];
    end
end

function newlist = fp_limit(list,strcontain)
% fp_limit - takes a cell array of strings (i.e. filepaths) and limits to
% ones which contain a certain string.

% This will take an array of files and prune the result to a list that
% CONTAINS the string variable strcontain.

newlist = list(~cellfun('isempty',strfind(list,strcontain)));