FROM rockylinux:8.9

# We need a few additional packages for installations, xvfb, imagemagick, freesurfer, matlab
# procps-ng provides uptime
RUN yum -y update && \
    yum -y install findutils wget zip unzip which procps-ng python3 && \
    yum -y install epel-release && \
    yum -y install ImageMagick && \
    yum -y install xorg-x11-server-Xvfb xorg-x11-xauth && \
    yum -y install procps-ng mesa-libGLU fontconfig libtiff mesa-dri-drivers && \
    yum -y install java-1.8.0-openjdk && \
    yum clean all

# FS RPM package
RUN cd /opt && \
    wget -q https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/8.1.0/freesurfer-Rocky8-8.1.0-1.x86_64.rpm && \
    yum -y install /opt/freesurfer-Rocky8-8.1.0-1.x86_64.rpm && \
    rm freesurfer-Rocky8-8.1.0-1.x86_64.rpm
ENV FREESURFER_HOME /usr/local/freesurfer/8.1.0-1

# Freesurfer environment
ENV FREESURFER ${FREESURFER_HOME}
ENV FREESURFER_HOME_FSPYTHON ${FREESURFER_HOME}
ENV SUBJECTS_DIR ${FREESURFER_HOME}/subjects
ENV MNI_DIR ${FREESURFER_HOME}/mni
ENV MNI_PERL5LIB ${FREESURFER_HOME}/mni/share/perl5
ENV MINC_BIN_DIR ${FREESURFER_HOME}/mni/bin
ENV MNI_DATAPATH ${FREESURFER_HOME}/mni/data
ENV FSFAST_HOME ${FREESURFER_HOME}/fsfast
ENV FSF_OUTPUT_FORMAT nii.gz
ENV LOCAL_DIR ${FREESURFER_HOME}/local
ENV FMRI_ANALYSIS_DIR ${FREESURFER_HOME}/fsfast
ENV FUNCTIONALS_DIR ${FREESURFER_HOME}/sessions
ENV PERL5LIB ${FREESURFER_HOME}/mni/share/perl5
ENV FS_OVERRIDE 0
ENV LESSOPEN "||/usr/bin/lesspipe.sh %s"
ENV FS_V8_XOPTS 1
ENV PATH /usr/local/freesurfer/8.1.0-1/mni/bin${PATH}
ENV PATH /usr/local/freesurfer/8.1.0-1/tktools:${PATH}
ENV PATH /usr/local/freesurfer/8.1.0-1/fsfast/bin:${PATH}
ENV PATH /usr/local/freesurfer/8.1.0-1/bin:${PATH}

# Scripts etc for NextBrain
RUN cd /opt && \
    wget https://github.com/freesurfer/freesurfer/archive/refs/tags/v8.1.0.zip && \
    unzip v8.1.0.zip && \
    mv freesurfer-8.1.0/mri_histo_util/ERC_bayesian_segmentation \
        ${FREESURFER_HOME}/python/packages && \
    rm -r v8.1.0.zip freesurfer-8.1.0

# Atlases for NextBrain
RUN cd /opt && \
    wget https://ftp.nmr.mgh.harvard.edu/pub/dist/lcnpublic/dist/Histo_Atlas_Iglesias_2023/atlas_simplified.zip && \
    unzip atlas_simplified.zip -d "${FREESURFER_HOME}"/python/packages/ERC_bayesian_segmentation && \
    rm atlas_simplified.zip

# Add modules to system python
RUN pip3 install pandas nibabel numpy scipy

# Matlab Compiled Runtime
RUN wget -nv https://ssd.mathworks.com/supportfiles/downloads/R2023a/Release/6/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2023a_Update_6_glnxa64.zip \
    -O /opt/mcr_installer.zip && \
    unzip /opt/mcr_installer.zip -d /opt/mcr_installer && \
    /opt/mcr_installer/install -mode silent -agreeToLicense yes && \
    rm -r /opt/mcr_installer /opt/mcr_installer.zip

# Matlab env
ENV MATLAB_SHELL=/bin/bash
ENV AGREE_TO_MATLAB_RUNTIME_LICENSE=yes
ENV MATLAB_RUNTIME=/usr/local/MATLAB/MATLAB_Runtime/R2023a
ENV MCR_INHIBIT_CTF_LOCK=1
ENV MCR_CACHE_ROOT=/tmp

# And add our own code for custom post-processing and QC
COPY README.md /opt/fs-extensions/
COPY src /opt/fs-extensions/src
ENV PATH /opt/fs-extensions/src:/opt/fs-extensions/matlab/bin:${PATH}

# Matlab executable must be run at build to extract the CTF archive
RUN run_matlab_entrypoint.sh ${MATLAB_RUNTIME} quit

# Entrypoint
ENTRYPOINT ["run-everything.sh"]
